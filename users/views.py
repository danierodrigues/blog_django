from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, UpdateView, ListView

from assets.queries.raw_queries import getProfilesListWithotThisUser, addFriend, removeFriend, isThisUserAFriend
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from .models import Profile


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UserListView(ListView):
    model = Profile
    template_name = 'registration/users_page.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(UserListView, self).get_context_data()
        profiles = getProfilesListWithotThisUser(self.request.user.id)
        for profile in profiles:
            profile.isFollower = profile.isFollowerFunction(self.request.user.id)
        context['users'] = profiles
        return context


class UserRegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')
    template_name = 'registration/change_password.html'

def password_success(request):
    return render(request, 'registration/password_success.html', {})

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, user_id=self.kwargs['pk'])
        total_friends = page_user.total_friends()

        isFollower = False
        if isThisUserAFriend(page_user, self.request.user.id):
            isFollower = True

        context['page_user'] = page_user
        context["total_friends"] = total_friends
        context["isFollower"] = isFollower
        return context

class EditProfilePageView(UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    form_class = ProfilePageForm
    success_url = reverse_lazy('home')

class CreateProfilePageView(CreateView):
    template_name = "registration/create_user_profile_page.html"
    form_class = ProfilePageForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def FriendView(request, pk):
    user = get_object_or_404(Profile, user_id=request.POST.get('friend_id'))
    if isThisUserAFriend(user, request.user.id):
        removeFriend(user, request.user)
    else:
        addFriend(user, request.user)

    return HttpResponseRedirect(reverse('show_profile_page', args=[str(pk)]))

def FriendAndRedirectToUserList(request):
    user = get_object_or_404(Profile, user_id=request.POST.get('friend_id'))
    if isThisUserAFriend(user, request.user.id):
        removeFriend(user, request.user)
    else:
        addFriend(user, request.user)

    return HttpResponseRedirect(reverse('index_user'))