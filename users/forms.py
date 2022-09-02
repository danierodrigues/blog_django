from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, ReadOnlyPasswordHashField
from django.contrib.auth.models import User
from django import forms

from assets.forms.error_messages import required, password_mismatch
from assets.forms.helper_text import username_digits, register_password, password_confirmation, helper_password
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), error_messages=(required))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Primeiro Nome', error_messages=(required))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Ultimo Nome', error_messages=(required))

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

        labels = {
            'username': 'Nome de Utilizador',
            'first_name': 'Primeiro Nome',
            'last_name': 'Ultimo Nome',
            'email': 'Email',
            'password1': 'Password',
            'password2': 'Confirmação de Password'
        }
        error_messages = {
            'username': (required),
            'password1': (required),
            'password2': (required, password_mismatch),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = username_digits
        self.fields['password2'].help_text = password_confirmation
        self.fields['password1'].help_text = helper_password


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email', error_messages=(required))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Primeiro Nome', error_messages=(required))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), label='Ultimo Nome', error_messages=(required))
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=(register_password))

    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email')

        labels = {
            'first_name': 'Primeiro Nome',
            'last_name': 'Ultimo Nome',
            'email': 'Email'
        }


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label='Password atual', error_messages=(required))
    new_password1 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label='Nova Password', error_messages=(required))
    new_password2 = forms.CharField(max_length=100,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}), label='Confirmação de nova Password', error_messages=(required))

    class Meta():
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

        labels = {
            'old_password': 'Password atual',
            'password1': 'Nova Password',
            'password2': 'Confirmação de nova Password'
        }

class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_description', 'profile_pic')
        widgets = {
            'profile_description': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'profile_description': 'Descrição do Perfil',
            'profile_pic': 'Imagem de Perfil'
        }
        error_messages = {
            'profile_description': (required),
        }
