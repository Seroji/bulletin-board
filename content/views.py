from typing import Any, Dict
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.views import generic, View

from rest_framework import generics

from .models import Post, Comment, Reply, PostUserFavourite, PostUserLike


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        follow_posts = PostUserFavourite.objects.filter(follower=self.request.user).values_list('post_id', flat=True)
        liked_posts = PostUserLike.objects.filter(liker=self.request.user).values_list('post_id', flat=True)
        context['follow_posts'] = follow_posts
        context['liked_posts'] = liked_posts
        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        user_id = self.request.user.id
        post_id = self.kwargs['pk']
        is_user_follower = PostUserFavourite.objects.filter(post_id=post_id, follower_id=user_id).exists()
        is_user_like = PostUserLike.objects.filter(post_id=post_id, liker_id=user_id).exists()
        context['is_user_follower'] = is_user_follower
        context['is_user_like'] = is_user_like
        return context


#htmx
class FollowThePostView(View):
    def post(self, request, *args, **kwargs):
        post_id = self.request.POST.get('id')
        user_id = self.request.user.id
        if not PostUserFavourite.objects.filter(follower_id=user_id, post_id=post_id).exists():
            obj = PostUserFavourite.objects.create(
                follower_id=user_id,
                post_id=post_id
            )
            obj.save()
            return render(self.request, 'htmx-responces/follow-responce-add.html')
        else:
            PostUserFavourite.objects.get(follower_id=user_id, post_id=post_id).delete()
            return render(self.request, 'htmx-responces/follow-responce-remove.html')
        

#htmx
class LikeThePostView(View):
    def post(self, request, *args, **kwargs):
        post_id = self.request.POST.get('like')
        user_id = self.request.user.id
        if not PostUserLike.objects.filter(liker_id=user_id, post_id=post_id).exists():
            obj = PostUserLike.objects.create(
                liker_id=user_id,
                post_id=post_id
            )
            obj.save()
            return render(self.request, 'htmx-responces/like-responce.html')
        else:
            PostUserLike.objects.get(liker_id=user_id, post_id=post_id).delete()
            return render(self.request, 'htmx-responces/dislike-responce.html')
        