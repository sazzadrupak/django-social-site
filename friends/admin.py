from django.contrib import admin

# Register your models here.
from . import models


class FriendAdmin(admin.ModelAdmin):
    list_display = ['user_one', 'user_two', 'friendship_status', 'lead_user']


admin.site.register(models.Friend, FriendAdmin)
