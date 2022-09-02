from django.shortcuts import render
from django.views.generic import ListView

from assets.queries.raw_queries import getPostsFiltered, getPublicPosts
from news.models import Posts

def index(request):
    context1 = {'post': Posts.objects.all()}
    return render(request, 'home_page.html', context1)

class PostListView(ListView):
    model = Posts
    template_name = 'home_page.html'
    context_object_name = 'posts'
    ordering = ['-date_published']

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data()
        if(self.request.user.id):
            context['posts'] = getPostsFiltered(self.request.user.id)
            print(context['posts'])
        else:
            context['posts'] = getPublicPosts()
        return context

def not_allowed(request):
    context = {}
    return render(request, 'not_allowed.html', context)