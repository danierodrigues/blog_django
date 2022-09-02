from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE, primary_key=True)
    profile_description = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    friends = models.ManyToManyField(User, related_name='friends')

    def total_friends(self):
        return self.friends.count()

    def isFollowerFunction(self,userId):
        return self.friends.filter(id=userId).exists()

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse('home')
