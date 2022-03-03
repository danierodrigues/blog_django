from django.urls import path

from .views import UserRegisterView, UserEditView, PasswordsChangeView, password_success, ShowProfilePageView, \
    EditProfilePageView, CreateProfilePageView, UserListView, FriendView, FriendAndRedirectToUserList

urlpatterns = [
    path('', UserListView.as_view(), name='index_user'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view()),
    path('password_success/', password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path('friend/<int:pk>', FriendView, name='friend-user'),
    path('friend/tousers', FriendAndRedirectToUserList, name='friend-user-to-users'),
]