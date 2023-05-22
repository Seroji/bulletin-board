import random

from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.category

class Post(models.Model):
    title = models.CharField(max_length=128)
    category = models.ManyToManyField(Category, 
                                      through='PostCategory')
    time_in = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,
                               related_name='posts', 
                               on_delete=models.CASCADE)
    content = HTMLField(default=None)
    cover = models.ImageField(upload_to='cover/')
    follow = models.ManyToManyField(User,
                                    through='PostUserFavourite',
                                    related_name='postsfollow')
    like = models.ManyToManyField(User,
                                  through='PostUserLike',
                                  related_name='postslike')


class PostCategory(models.Model):
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    

class PostUserFavourite(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE)
    

class PostUserLike(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    liker = models.ForeignKey(User,
                              on_delete=models.CASCADE)


class Reply(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    text = models.TextField(default='Отклик')
    answer = models.BooleanField(default=False)
    time_in = models.DateTimeField(auto_now_add=True)


class EmailAddresses(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)
    is_verify = models.BooleanField(default=False)
    otp = models.IntegerField(default='123456')

    @receiver(signal=post_save, sender=User)
    def create_email_check(sender, instance, created, **kwargs):
        if created:
            EmailAddresses.objects.create(
                user=instance,
                is_verify=False,
                otp=random.randrange(111111, 1000000)
            )
