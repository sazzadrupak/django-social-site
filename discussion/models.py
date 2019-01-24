from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class DiscussionHead(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='head_created_by')
    head_name = models.TextField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.head_name


class DiscussionUserGroup(models.Model):
    discussion_head = models.ForeignKey('discussion.DiscussionHead', on_delete=models.CASCADE,
                                        related_name='head_users')
    discussion_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discussion_user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Discussion(models.Model):
    discussion_head = models.ForeignKey('discussion.DiscussionHead', on_delete=models.CASCADE,
                                        related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_user_id')
    message = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


class DiscussionRecipient(models.Model):
    discussion = models.ForeignKey('discussion.Discussion', on_delete=models.CASCADE, related_name='discussion')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_user_id')
    is_read = models.BooleanField(default=False)
    discussion_head = models.ForeignKey('discussion.DiscussionHead', on_delete=models.CASCADE,
                                        related_name='message_head')

