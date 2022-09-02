from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from groups.models import Group


class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    post_title = models.CharField(max_length=200, null=False)
    post_content = RichTextField(blank=True, null=True)
    date_published = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    isPublic = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name='groups', blank=True)
    isForFollowers = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()

    def getImages(self):
        return Image.objects.filter(post_id=self.id)

    def hasImages(self):
        return Image.objects.filter(post_id=self.id).exists()

    def get_absolute_url(self):
        return reverse('post-details', kwargs={'pk': str(self.id)})

class Image(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="images/")