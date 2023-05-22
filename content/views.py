from typing import Any, Optional
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render, HttpResponse, redirect
from django.views import generic, View
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User

from .models import Post, Reply, PostUserFavourite, PostUserLike, PostCategory, Reply, EmailAddresses
from .forms import ProfileChangeForm, PasswordEditForm, PostAddForm, ReplyAddForm, OTPForm, AdvertismentForm
from .filters import ReplyFilter
from .tasks import reply_info, apply_info, verify_email, advert


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
    
    def get_queryset(self):
        return Post.objects.all().order_by('-id')   


class MainProfileView(LoginRequiredMixin, generic.DetailView):
    def get(self, request):
        res = EmailAddresses.objects.filter(user=self.request.user, is_verify=True).exists()
        return render(request, "profile/profile.html", {'email_verified': res})
    

#htmx
class MainProfileGetView(LoginRequiredMixin, View):
    def get(self, request):
        res = EmailAddresses.objects.filter(user=self.request.user, is_verify=True).exists()
        return render(request, 'partials/profile_main.html', {'email_verified': res})
    

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
            apply_info.delay(reply_id=reply_id)
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
            is_author_current_user = Post.objects.filter(author=user, id=post_id).exists()
            context['is_user_follower'] = is_user_follower
            context['is_user_like'] = is_user_like
            context['is_user_reply'] = is_user_reply
            context['is_author_current_user'] = is_author_current_user
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
        reply_info.delay(post_id=post_id)
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
        if not self.request.user.groups.filter(name='virified_email').exists():
            form = OTPForm()
            return redirect(to='verify_email')
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
    

class ChangePostView(generic.UpdateView):
    form_class = PostAddForm
    model = Post
    template_name = 'post_add.html'
    success_url = reverse_lazy('main_page')

    def get(self, request, *args, **kwargs):
        if EmailAddresses.objects.filter(user_id=self.request.user.id, is_verify=False).exists():
            form = OTPForm()
            verify_email.delay(user_id=self.request.user.id)
            return redirect(to='verify_email')
        instance = Post.objects.get(id=kwargs.pop('pk'))
        form = PostAddForm(instance=instance)
        return render(self.request, 'post_add.html', {'form': form})


class VerifyEmailByCodeView(View):
    def get(self, request, *args, **kwargs):
        if EmailAddresses.objects.filter(user_id=self.request.user.id, is_verify=False).exists():
            form = OTPForm()
            verify_email.delay(user_id=self.request.user.id)
            return render(self.request, 'profile/verify_email.html', {'form': form})
        else:
            return redirect(to='main_page')
    
    def post(self, request, *args, **kwargs):
        otp = int(self.request.POST['otp'])
        instance = EmailAddresses.objects.get(user_id=self.request.user.id)
        otp_base = instance.otp
        if otp == otp_base:
            instance.is_verify = True
            instance.save()
            group = Group.objects.get(id=1)
            group.user_set.add(self.request.user)
            return redirect(to='main_profile')
        else:
            form = OTPForm()
            message = 'Неверный код!'
            return render(self.request, 'profile/verify_email.html', {'form': form, 'message': message})


class FavouritePostView(View):
    def get(self, request, *args, **kwargs):
        posts = []
        posts_ids = PostUserFavourite.objects.filter(follower=self.request.user).values_list('post_id', flat=True)
        for pk in posts_ids:
            post = Post.objects.get(pk=pk)
            posts.append(post)
        context = {
            'posts': posts,
        }
        return render(self.request, 'follow_post.html', context=context)


class AdvertismentView(View):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            form = AdvertismentForm()
            return render(request, 'advertisment.html', {'form': form})
        else:
            return redirect(to='main_page')
    
    def post(self, request, *args, **kwargs):
        subject = request.POST['subject']
        text_content = request.POST['text_content']
        advert.delay(subject=subject, text_content=text_content)
        return redirect(to='main_page')
