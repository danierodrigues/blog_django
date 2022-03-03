from django import forms
from .models import Group


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'description', 'group_picture')


        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }
        labels = {
            'name': 'Name',
            'description': 'Description'
        }
