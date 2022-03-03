from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    post_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Post
        fields = ('post_title', 'post_content', 'post_image', 'isPublic', 'isForGroups', 'isForFollowers')


        widgets = {
            'post_title': forms.TextInput(attrs={'class': 'form-control'}),
            'post_content': forms.Textarea(attrs={'class': 'form-control'}),
            #'post_image': forms.ClearableFileInput(attrs={'multiple': True})
        }
        labels = {
            'post_title': 'Title',
            'post_content': 'Content',
            'isPublic': 'Public access',
            'isForGroups': 'My Groups access',
            'isForFollowers': 'My Followers access'
        }
