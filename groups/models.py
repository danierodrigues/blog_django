from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Group(models.Model):
    owner = models.OneToOneField(User, null=False, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)
    description = RichTextField(blank=True, null=True, max_length=300)
    group_picture = models.ImageField(null=True, blank=True, upload_to="images/groups/")
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    users = models.ManyToManyField(User, related_name='users', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def total_users(self):
        return self.users.count() + 1

    def get_absolute_url(self):
        return reverse('group-details', kwargs={'pk': str(self.id)})