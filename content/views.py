from typing import Any, Dict, List
from django.shortcuts import render, HttpResponse
from django.views import generic, View

from .models import Post, Comment, Reply


class MainPageView(generic.ListView):
    model = Post
    context_object_name = 'announcements'
    template_name = 'main_page.html'
    paginate_by = 1   #Поменять порядок новостей

    def get_template_names(self):
        if self.request.htmx:
            return 'partials/main_page_elements.html'
        return 'main_page.html'

class OwnProfileView(View):
    def get(self, request):
        return render(request, 'profile/profile.html')
    

class OwnProfileStaticticView(View):
    def get(self, request):
        pk = request.user.id
        return HttpResponse('1233345')
