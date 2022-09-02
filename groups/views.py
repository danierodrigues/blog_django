from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404

from assets.queries.raw_queries import getAllUsersExceptSelf, getAllUsersExceptSelfAndOwner, userBelongsToThisGroup, \
    removeUserFromGroup, addUserToGroup
from .models import Group
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from .forms import GroupForm
from django.urls import reverse_lazy, reverse


def index(request):
    return HttpResponse("Hello, world. Groups Page")

class GroupListView(ListView):
    model = Group
    template_name = 'groups/groups_page.html'
    context_object_name = 'groups'
    ordering = ['-date_created']

    def get_context_data(self, **kwargs):
        context = super(GroupListView, self).get_context_data()
        groups = context['groups']
        for group in groups:
            print(group)
            fields = get_object_or_404(Group, id=group.id)
            total_users = group.total_users()
            entered = False
            if userBelongsToThisGroup(fields, self.request.user.id):
                entered = True

            group.total_users = total_users
            group.entered = entered
        return context


class AddGroupView(CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/create_group.html'

    def get_context_data(self, **kwargs):
        context = super(AddGroupView, self).get_context_data()

        users = getAllUsersExceptSelf(self.request.user.id)

        form = context['form']
        form.fields['users'].queryset = users.all()
        context['users'] = users
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        form.instance.owner = self.request.user

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('index_groups'))


class GroupDetailView(DetailView):
    model = Group
    template_name = 'groups/group_details.html'

    def get_context_data(self, **kwargs):
        context = super(GroupDetailView, self).get_context_data()
        fields = get_object_or_404(Group, id=self.kwargs['pk'])
        total_users = fields.total_users()

        entered = False
        if userBelongsToThisGroup(fields, self.request.user.id):
            entered = True

        context["total_users"] = total_users
        context["entered"] = entered
        return context

class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'groups/update_group.html'

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data()
        fields = get_object_or_404(Group, id=self.kwargs['pk'])

        users = getAllUsersExceptSelfAndOwner(self.request.user.id, fields.owner_id)

        form = context['form']
        form.fields['users'].queryset = users.all()
        context['users'] = users
        return context

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'groups/delete_group.html'
    success_url = reverse_lazy('index_groups')

def EnterUserView(request, pk):
    group = get_object_or_404(Group, id=request.POST.get('group_id'))

    if userBelongsToThisGroup(group, request.user.id):
        removeUserFromGroup(group, request.user)

    else:
        addUserToGroup(group, request.user)


    return HttpResponseRedirect(reverse('group-details', args=[str(pk)]))

def EnterInGroupAndRedirectToGroupList(request):
    group = get_object_or_404(Group, id=request.POST.get('group_id'))
    if userBelongsToThisGroup(group, request.user.id):
        removeUserFromGroup(group, request.user)
    else:
        addUserToGroup(group, request.user)

    return HttpResponseRedirect(reverse('index_groups'))