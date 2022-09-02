from django.urls import path
from .views import AddGroupView, GroupListView, GroupDeleteView, GroupUpdateView, GroupDetailView, EnterUserView, EnterInGroupAndRedirectToGroupList

urlpatterns = [
    path('', GroupListView.as_view(), name='index_groups'),
    path('group/', AddGroupView.as_view(), name='group-create'),
    path('groupdetail/<int:pk>', GroupDetailView.as_view(), name='group-details'),
    path('group/edit/<int:pk>', GroupUpdateView.as_view(), name='group-update'),
    path('group/<int:pk>/delete', GroupDeleteView.as_view(), name='group-delete'),
    path('user/<int:pk>', EnterUserView, name='group-user'),
    path('users/entergroup', EnterInGroupAndRedirectToGroupList, name='group-user-to-users'),
]