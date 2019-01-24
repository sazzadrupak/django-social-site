from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser

FRIENDSHIP_STATUS_CHOICES = (
    (0, 'Pending'),
    (1, 'Accepted'),
)


class Friend(models.Model):
    user_one = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_one_id')
    user_two = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_two_id')
    friendship_status = models.IntegerField(default=0, choices=FRIENDSHIP_STATUS_CHOICES)
    lead_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lead_user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user_one', 'user_two',)


