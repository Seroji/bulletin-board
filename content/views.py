from django.shortcuts import render
from django.views import generic

from .models import Post, Comment


class MainPageView(generic.ListView):
    model = Post
    

