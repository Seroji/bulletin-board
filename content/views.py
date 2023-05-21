from typing import Any, Optional
from django.db import models
from django.shortcuts import render, HttpResponse, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Reply, PostUserFavourite, PostUserLike, PostCategory, Reply
from .forms import ProfileChangeForm, PasswordEditForm, PostAddForm, ReplyAddForm
from .filters import ReplyFilter

from django.core.mail import send_mail


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
        if self.request.user.is_authenticated:
            follow_posts = PostUserFavourite.objects.filter(follower=self.request.user).values_list('post_id', flat=True)
            liked_posts = PostUserLike.objects.filter(liker=self.request.user).values_list('post_id', flat=True)
            context['follow_posts'] = follow_posts
            context['liked_posts'] = liked_posts
        return context


class MainProfileView(LoginRequiredMixin, generic.DetailView):
    def get(self, request):
        return render(request, "profile/profile.html")
    

#htmx
class MainProfileGetView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'partials/profile_main.html')
    

#htmx
class StatProfileGetView(LoginRequiredMixin, View):
    def get(self, request):
        count = 0
        all_posts = Post.objects.filter(author_id=self.request.user.id)
        for post in all_posts:
            count += Reply.objects.filter(post=post).count()
        context = {
            'total_replies': count,
        }
        return render(request, 'partials/profile_stat.html', context=context)
    

class TotalRepliesView(LoginRequiredMixin, View):
    def get(self, request):
        replies = Reply.objects.filter(post__author=self.request.user)
        reply_filter = ReplyFilter(request.GET, queryset=replies)
        context = {
            'filter': reply_filter,
        }
        return render(request, 'total_replies.html', context=context)
    
    def get_users(request):
        return Reply.objects.all()
    

class ReplyActionView(View):
    def post(self, request, *args, **kwargs):
        reply_id = self.request.POST.get('obj-id')
        reply = Reply.objects.get(id=reply_id)
        if 'apply' in self.request.POST:
            reply.answer = True
            reply.save()
            return HttpResponse('<span style="color: green">Принят</span>')
        if 'deny' in self.request.POST:
            reply.delete()
            return HttpResponse('<span style="color: red">Отклонён</span>')


class PostDetailView(generic.DetailView, FormMixin):
    model = Post
    template_name = 'detail_view.html'
    context_object_name = 'obj'
    form_class = ReplyAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.request.user.is_authenticated:
            user = self.request.user
            post_id = self.kwargs['pk']
            is_user_follower = PostUserFavourite.objects.filter(post_id=post_id, follower=user).exists()
            is_user_like = PostUserLike.objects.filter(post_id=post_id, liker=user).exists()
            is_user_reply = Reply.objects.filter(author=user, post_id=post_id).exists()
            context['is_user_follower'] = is_user_follower
            context['is_user_like'] = is_user_like
            context['is_user_reply'] = is_user_reply
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReplyAddForm()
        post_id = self.kwargs['pk']
        user = self.request.user
        reply_text = self.request.POST['text']
        obj = Post.objects.get(pk=post_id)
        reply = Reply.objects.create(
            post_id=post_id,
            author=user,
            text=reply_text,
        )
        reply.save()
        is_user_follower = PostUserFavourite.objects.filter(post_id=post_id, follower=user).exists()
        is_user_like = PostUserLike.objects.filter(post_id=post_id, liker=user).exists()
        is_user_reply = Reply.objects.filter(author=user, post_id=post_id).exists()
        return render(request, self.template_name, {'obj':obj, 
                                                    'form': form, 
                                                    'is_user_follower': is_user_follower,
                                                    'is_user_like': is_user_like,
                                                    'is_user_reply': is_user_reply,})


#htmx
class FollowThePostView(LoginRequiredMixin, View):
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
class LikeThePostView(LoginRequiredMixin, View):
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
        

class ProfileChangeView(LoginRequiredMixin, generic.UpdateView):
    form_class = ProfileChangeForm
    template_name = 'profile/profile_change.html'
    success_url = reverse_lazy('after_change')

    def get_object(self):
        return self.request.user
        

#htmx
class AfterChangeProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(self.request, 'partials/after_change_profile.html')


class PasswordEditView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordEditForm
    template_name = 'profile/password_change.html'
    success_url = reverse_lazy('main_profile')


class PostAddView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostAddForm
    template_name = 'post_add.html'
    success_url = reverse_lazy('main_page')

    def post(self, request, *args, **kwargs):
        form = PostAddForm(request.POST, request.FILES)
        if not request.FILES:
            print('123')
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
        announcements = Post.objects.all()
        return redirect(to='main_page')
