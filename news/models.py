from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=200, null=False)
    post_content = RichTextField(blank=True, null=True)
    date_published = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blog_posts')
    isPublic = models.BooleanField(default=True)
    isForGroups = models.BooleanField(default=False)
    isForFollowers = models.BooleanField(default=False)

    def total_likes(self):
        return self.likes.count()


    def get_absolute_url(self):
        return reverse('post-details', kwargs={'pk': str(self.id)})

class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="images/")