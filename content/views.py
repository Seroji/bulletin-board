from typing import Any, Optional
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponse
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView

from .models import Post, Reply, PostUserFavourite, PostUserLike, PostCategory
from .forms import ProfileChangeForm, PasswordEditForm, PostAddForm


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
        

class ProfileChangeView(generic.UpdateView):
    form_class = ProfileChangeForm
    template_name = 'profile/profile_change.html'
    success_url = reverse_lazy('after_change')

    def get_object(self):
        return self.request.user
        

#htmx
class AfterChangeProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'partials/after_change_profile.html')


class PasswordEditView(PasswordChangeView):
    form_class = PasswordEditForm
    template_name = 'profile/password_change.html'
    success_url = reverse_lazy('main_profile')


class PostAddView(generic.CreateView):
    model = Post
    form_class = PostAddForm
    template_name = 'post_add.html'
    success_url = reverse_lazy('main_page')

    def post(self, request, *args, **kwargs):
        form = PostAddForm(request.POST, request.FILES)
        if not request.FILES:
            return render(request, self.template_name, {'form': form})
        post = Post(
            title = request.POST['title'],
            author = self.request.user,
            content = request.POST['content'],
            cover = request.FILES['cover']
        )
        post.save()
        PostCategory.objects.create(
            post=post,
            category_id=request.POST['category'],
        )
        return HttpResponse('Success')
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': PostAddForm})
