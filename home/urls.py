from django.urls import path
from .views import PostListView, not_allowed

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('forbidden/', not_allowed, name='not_allowed'),
]