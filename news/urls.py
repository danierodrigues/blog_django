from django.urls import path, re_path
from .views import PostDetailView, AddPostView, PostUpdateView, PostDeleteView, LikeView, ImageView, ImageDeleteRequest

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/', AddPostView.as_view(), name='post'),
    path('postdetail/<int:pk>', PostDetailView.as_view(), name='post-details'),
    path('post/edit/<int:pk>', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>', LikeView, name='post-like'),
    path('image/<int:pk>', ImageView.as_view(), name='post-image'),
    path('image/<int:pk>/delete', ImageDeleteRequest, name='image-delete'),
]