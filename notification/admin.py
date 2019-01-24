from django.contrib import admin

# Register your models here.
from . import models


class NotificationAdmin(admin.ModelAdmin):
    search_fields = ['to_user', 'from_user', 'notification_text', 'post_status', 'created_at']
    list_display = ['to_user', 'from_user', 'notification_text', 'post_status', 'created_at']


admin.site.register(models.Notification, NotificationAdmin)