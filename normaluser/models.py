from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models

GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female')
)


class NormalUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='m')
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=16)
    birth_date = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_image', blank=True)
    email_validation_code = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username

