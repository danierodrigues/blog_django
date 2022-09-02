from django import forms
from easy_select2 import Select2Multiple
from easy_select2 import select2_modelform

from assets.forms.error_messages import required
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'group_picture', 'users')


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'users': forms.CheckboxSelectMultiple(
                attrs={'id': 'users','required': False}
            )
        }
        labels = {
            'name': 'Nome*',
            'description': 'Descrição*',
            'group_picture': 'Imagem do Grupo',
            'users': 'Utilizadores'
        }
        error_messages = {
            'name': (required),
            'description': (required),
        }
        required={
            'group_picture':False
        }
