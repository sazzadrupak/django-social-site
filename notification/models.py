from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user_id')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user_id')
    notification_text = models.TextField(null=False, blank=False, max_length=255)
    post_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.notification_text
