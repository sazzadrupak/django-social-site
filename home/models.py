from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    post_text = models.TextField(max_length=200)
    post_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]

    def __str__(self):
        return self.post_text


class Comment(models.Model):
    post = models.ForeignKey('home.Post', on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at', ]

    def __str__(self):
        return self.comment_text



