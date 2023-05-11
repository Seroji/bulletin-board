from typing import Any, Dict
from django.shortcuts import render
from django.views import generic, View

from .models import Post, Comment, Reply


class MainPageView(generic.ListView):
    model = Post
    context_object_name = 'announcements'
    template_name = 'main_page.html'


class OwnProfileView(View):
    def get(self, request):
        return render(request, 'profile/profile.html')
    

class OwnProfileStaticticView(View):
    def get(self, request):
        pk = request.user.id
        total_replies = Reply.objects.filter().count()
