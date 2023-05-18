from typing import Any, Dict
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.core.exceptions import ValidationError
from django import forms

from tinymce.widgets import TinyMCE
from image_uploader_widget.widgets import ImageUploaderWidget

from .models import Post


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
