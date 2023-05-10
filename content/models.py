from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=128)
    category = models.ManyToManyField(Category, through='PostCategory')
    time_in = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,
                               related_name='posts', 
                               on_delete=models.CASCADE)
    like = models.PositiveIntegerField(default=0)
    content = HTMLField(default=None)


class PostCategory(models.Model):
    category = models.ForeignKey(Category, 
                                 on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    like = models.PositiveIntegerField(default=0)
    post = models.ForeignKey(Post,
                             related_name="comments",
                             on_delete=models.CASCADE)
