from django.contrib.auth.models import User
from django import forms

import django_filters

from .models import Reply

class DateInput(forms.DateInput):
    input_type = 'date'


class ReplyFilter(django_filters.FilterSet):
    author = django_filters.ModelChoiceFilter(queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    time_in = django_filters.DateFilter(label='Позже, чем', field_name='time_in', lookup_expr='gt', widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    post = django_filters.CharFilter(label='Заголовок публикации', field_name='post__title', lookup_expr='icontains', widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Reply
        fields = [
            'author',
            'time_in',
            'post',
        ]
