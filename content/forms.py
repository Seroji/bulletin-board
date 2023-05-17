from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django import forms


class ProfileChangeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    last_name = forms.CharField(max_length=50, label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    username = forms.CharField(max_length=50, label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    email = forms.EmailField(label='Электронная почта', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'email'}))

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
        )


class PasswordEditForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password1',
            'new_password2',
        )
