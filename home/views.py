from django.shortcuts import render
from django.views.generic import ListView
from news.models import Post

def index(request):
    context1 = {'post': Post.objects.all()}
    return render(request, 'home_page.html', context1)

class PostListView(ListView):
    model = Post
    template_name = 'home_page.html'
    context_object_name = 'post'
    ordering = ['-date_published']

def not_allowed(request):
    context = {}
    return render(request, 'not_allowed.html', context)