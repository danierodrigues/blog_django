from django import forms

from assets.forms.error_messages import required
from .models import Posts, Image


class PostForm(forms.ModelForm):
    post_image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'label': 'Imagens'}),
        label='Adicionar Imagem',
        required=False
    )

    class Meta:
        model = Posts
        fields = ('post_title', 'post_content', 'post_image', 'isPublic', 'groups', 'isForFollowers')


        widgets = {
            'post_title': forms.TextInput(attrs={'class': 'form-control'}),
            'post_content': forms.Textarea(attrs={'class': 'form-control'}),
            'groups': forms.CheckboxSelectMultiple(
                attrs={'id': 'groups', 'required': False}
            )
        }
        labels = {
            'post_title': 'Titulo*',
            'post_content': 'Descrição*',
            'isPublic': 'Acesso Publico',
            'isForFollowers': 'Acesso aos meus seguidores',
            'groups': 'Grupos'
        }
        error_messages = {
            'post_title': (required),
            'post_content': (required),
        }

class PostFormUpdate(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ('post_title', 'post_content', 'isPublic', 'groups', 'isForFollowers')


        widgets = {
            'post_title': forms.TextInput(attrs={'class': 'form-control'}),
            'post_content': forms.Textarea(attrs={'class': 'form-control'}),
            'groups': forms.CheckboxSelectMultiple(
                attrs={'id': 'groups', 'required': False}
            )
        }
        labels = {
            'post_title': 'Titulo*',
            'post_content': 'Descrição*',
            'isPublic': 'Acesso Publico',
            'isForFollowers': 'Acesso aos meus seguidores',
            'groups': 'Grupos'
        }
        error_messages = {
            'post_title': (required),
            'post_content': (required),
        }



class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)


        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True})
        }
        labels = {
            'image': 'Imagens'
        }

