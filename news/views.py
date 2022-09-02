from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, TemplateView

from assets.queries.raw_queries import getAllGroupsOfThisUser, haveaccessToPostPublicOrGroupsOrFollowers, \
    isPostOwnerCheck, updatePostById, getPostByPostId, groupBelongsToPost, createImagePost, getPostByPostIdWithGet, \
    getImagePostByPostId, postLikedByThisUser, removeGroupToPost, addGroupToPost, removeLikeToPost, addLikeToPost, \
    deleteImage
from .models import Posts, Image
from .forms import PostForm, ImageForm, PostFormUpdate
from django.urls import reverse_lazy, reverse


def index(request):
    return HttpResponse("Hello, world. News Page")

class AddPostView(CreateView):
    model = Posts
    form_class = PostForm
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super(AddPostView, self).get_context_data()

        groups = getAllGroupsOfThisUser(self.request.user.id)

        form = context['form']
        form.fields['groups'].queryset = groups.all()
        context['groups'] = groups
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        form.instance.author = self.request.user


        images = self.request.FILES.getlist('post_image')
        if form.is_valid():
            form.save()
            for img in images:
                createImagePost(form.instance, img)

            return redirect(reverse('post-details', kwargs={'pk': str(form.instance.id) }))

        groups = getAllGroupsOfThisUser(self.request.user.id)
        groups.queryset = groups.all()
        context = {'form': form, 'groups': groups}
        return render(request, 'post.html', context)


class PostDetailView(DetailView):
    model = Posts
    template_name = 'post_details.html'

    def get(self, *args, **kwargs):
        context = getPostByPostIdWithGet(kwargs['pk'])
        accessAllowed = haveaccessToPostPublicOrGroupsOrFollowers(context.id, self.request.user.id)
        if not accessAllowed:
            return HttpResponseRedirect(reverse('not_allowed'))

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        fields = get_object_or_404(Posts, id=self.kwargs['pk'])
        total_likes = fields.total_likes()
        images = getImagePostByPostId(self.kwargs['pk'])#Image.objects.filter(post_id=self.kwargs['pk'])
        liked = False
        if postLikedByThisUser(fields, self.request.user.id): #fields.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        context["images"] = images
        return context

class PostUpdateView(UpdateView):
    model = Posts
    form_class = PostFormUpdate
    template_name = 'update_post.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data()
        fields = get_object_or_404(Posts, id=self.kwargs['pk'])
        groups = getAllGroupsOfThisUser(self.request.user.id)

        form = context['form']
        form.fields['groups'].queryset = groups.all()
        context['allGroups'] = fields.groups
        return context

    def post(self, request, *args, **kwargs):
        form = PostFormUpdate(request.POST)
        post = getPostByPostId(self.kwargs['pk'])
        groupsOfThisUser = getAllGroupsOfThisUser(self.request.user.id)

        if form.is_valid():
            updatePostById(self.kwargs['pk'], form.instance)

            selected_groups = form.cleaned_data['groups']
            for groupOfThisUser in groupsOfThisUser:
                haveGroup = groupBelongsToPost(self.kwargs['pk'], groupOfThisUser.id)
                if groupOfThisUser in selected_groups:
                    if not haveGroup:
                        addGroupToPost(post, groupOfThisUser)
                else:
                    if haveGroup:
                        removeGroupToPost(post, groupOfThisUser)

            return redirect(reverse('post-details', kwargs={'pk': str(self.kwargs['pk'])}))

        groups = getAllGroupsOfThisUser(self.request.user.id)
        groups.queryset = groups.all()
        context = {'form': form, 'groups': groups}
        return render(request, 'post.html', context)



class PostDeleteView(DeleteView):
    model = Posts
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

def LikeView(request, pk):
    post = get_object_or_404(Posts, id=pk)
    if postLikedByThisUser(post, request.user.id):
        removeLikeToPost(post, request.user)
    else:
        addLikeToPost(post, request.user)

    return HttpResponseRedirect(reverse('post-details', args=[str(pk)]))


class ImageView(CreateView):
    model = Image
    form_class = ImageForm
    template_name = 'images/update_images.html'

    def get_context_data(self, **kwargs):
        context = super(ImageView, self).get_context_data()
        images = getImagePostByPostId(self.kwargs['pk'])

        postObject = isPostOwnerCheck(self.request.user.id, self.kwargs['pk'])

        if (not postObject):
            context['not_authorized'] = True
            return context

        context['images'] = images
        return context


    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST, request.FILES)
        postObject = isPostOwnerCheck(self.request.user.id, self.kwargs['pk'])

        if(not postObject):
            return HttpResponseRedirect(reverse('not_allowed'))

        images = self.request.FILES.getlist('image')
        if form.is_valid():
            form.save()
            for img in images:
                createImagePost(postObject, img)

            return redirect(reverse('post-image', kwargs={'pk': str(postObject.id)}))

        return HttpResponseRedirect(reverse('post-image', args=[str(postObject.id)]))

def ImageDeleteRequest(request, pk):
    image = get_object_or_404(Image, id=pk)
    isPostOwner = isPostOwnerCheck(request.user.id, image.post_id)
    if(isPostOwner):
        deleteImage(image)
        return HttpResponseRedirect(reverse('post-image', args=[str(image.post_id)]))
    else:
        return HttpResponseRedirect(reverse('not_allowed'))

