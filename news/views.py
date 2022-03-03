from django.db.models import Q, When
from django.http import HttpResponse, request, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Image
from .forms import PostForm
from django.urls import reverse_lazy, reverse
from groups.models import Group
from users.models import Profile


def index(request):
    return HttpResponse("Hello, world. News Page")

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post.html'

    def post(self, request, *args, **kwargs):
        #form = self.form_class(request.POST)
        form = PostForm(request.POST, request.FILES)
        form.instance.author = self.request.user

        images = self.request.FILES.getlist('post_image')
        if form.is_valid():
            print("chegou aqui")

            form.save()
            for img in images:
                print("passou aqui no for")
                Image.objects.create(post=form.instance, image=img)

            return redirect(reverse('post-details', kwargs={'pk': str(form.instance.id) }))

        context = {'form': form}
        return render(request, 'post.html', context)


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'

    def get(self, *args, **kwargs):
        context = Post.objects.get(pk=kwargs['pk'])

        accessAllowed = False
        print(self.request.user.is_authenticated)
        print(not context.isPublic and not self.request.user.is_authenticated)
        print(context.author)

        if context.isPublic and self.request.user.is_authenticated:
            accessAllowed = True
        elif not self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('not_allowed'))

        groups_allowed = Group.objects.filter(Q(users=context.author) and Q(users=self.request.user))
        print(groups_allowed)

        followers_allowed = Profile.objects.filter(user_id=self.request.user, friends=context.author)
        print(followers_allowed)
        if (groups_allowed and context.isForGroups) or (followers_allowed and context.isForFollowers):
            accessAllowed = True
        if not accessAllowed:
            return HttpResponseRedirect(reverse('not_allowed'))

        return super().get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data()
        fields = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = fields.total_likes()
        images = Image.objects.filter(post_id=self.kwargs['pk'])
        liked = False
        if fields.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["total_likes"] = total_likes
        context["liked"] = liked
        context["images"] = images
        return context

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'update_post.html'

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('post-details', args=[str(pk)]))