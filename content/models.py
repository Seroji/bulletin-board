from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time_in = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User,
                               related_name='posts', 
                               on_delete=models.CASCADE)
    content = HTMLField(default=None)


class Comment(models.Model):
    author = models.ForeignKey(User,
                               related_name='comments',
                               on_delete=models.CASCADE)
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post,
                             related_name="comments",
                             on_delete=models.CASCADE)
