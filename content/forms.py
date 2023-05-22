from typing import Any, Dict
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm

from tinymce.widgets import TinyMCE
from image_uploader_widget.widgets import ImageUploaderWidget
from allauth.account.forms import LoginForm

from .models import Post, Reply


CHOICES_CATEGORY = [
    (1, 'Танки'),
    (2, 'Хилы'),
    (3, 'ДД'),
    (4, 'Торговцы'),
    (5, 'Гилдмастеры'),
    (6, 'Квестгиверы'),
    (7, 'Кузнецы'),
    (8, 'Кожевники'),
    (9, 'Зельевары'),
    (10, 'Мастера заклинаний'),
]


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


class PostAddForm(forms.ModelForm):
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    content = forms.CharField(label='Содержание', widget=TinyMCE())
    category = forms.ChoiceField(
                                label='Категория',
                                choices=CHOICES_CATEGORY,
                                 widget=forms.Select(attrs={'class': 'form-select form-select-sm'}))
    cover = forms.ImageField(label='Обложка', widget=ImageUploaderWidget, required=False)
    class Meta:
        model = Post
        fields = (
            'cover',
            'title',
            'category',
            'content',
        )


class ReplyAddForm(forms.ModelForm):
    text = forms.CharField(label='Ваш отклик:', widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'text',}))
    class Meta:
        model = Reply
        fields = (
            'text',
        )

    
class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs.update({
            'class': 'form-control mx-auto',
            'type': 'email',
            'style':'width:500px',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control mx-auto',
            'type': 'password',
            'style':'width:500px',
        })


class CustomRegisterForm(UserCreationForm):
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'style': 'width:500px'}), required=True)
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'style': 'width:500px'}), required=True)
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'style': 'width:500px'}))
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'style': 'width:500px'}), required=True)
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:500px'}), required=True)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:500px'}), required=True)
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        )


class OTPForm(forms.Form):
    otp = forms.IntegerField(label='Проверочный код', 
                             widget=forms.TextInput(attrs={'class': 'form-control verify-code', 'type': 'text'}), 
                             required=True)


class AdvertismentForm(forms.Form):
    subject = forms.CharField(label='Тема письма', widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text'}))
    text_content = forms.CharField(label='Содержание', widget=forms.Textarea(attrs={'class': 'form-control', 'type': 'text'}))
