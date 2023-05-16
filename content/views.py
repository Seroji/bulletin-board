from typing import Any, Dict, List
from django.shortcuts import render, HttpResponse
from django.views import generic, View

from .models import Post, Comment, Reply


class MainPageView(generic.ListView):
    model = Post
    context_object_name = "announcements"
    template_name = "main_page.html"
    paginate_by = 1  # Поменять порядок новостей

    def get_template_names(self):
        self.template_name
        if self.request.htmx:
            return "partials/main_page_elements.html"
        return "main_page.html"


class MainProfileView(generic.DetailView):
    def get(self, request):
        return render(request, "profile/profile.html")
    

#htmx
class MainProfileGetView(View):
    def get(self, request):
        return render(request, 'partials/profile_main.html')
    

#htmx
class StatProfileGetView(View):
    def get(self, request):
        count = 0
        all_posts = Post.objects.filter(author_id=self.request.user.id)
        for post in all_posts:
            count += Reply.objects.filter(post=post).count()
        context = {
            'total_replies': count,
        }
        return render(request, 'partials/profile_stat.html', context=context)
    

class TotalRepleisView(View):
    def get(self, request):
        replies = []
        all_posts = Post.objects.filter(author_id=self.request.user.id)
        for post in all_posts:
            obj = Reply.objects.all().filter(post=post)
            if obj:
                replies.append(obj[0])
        context = {
            'replies': replies,
        }
        print(replies)
        return render(request, 'total_replies.html', context=context)
    


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'detail_view.html'
    context_object_name = 'obj'