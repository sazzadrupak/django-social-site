from django.contrib import admin

# Register your models here.
from . import models


class DiscussionInline(admin.TabularInline):
    model = models.Discussion


class DiscussionUserGroupInline(admin.TabularInline):
    model = models.Discussion


class DiscussionRecipientInline(admin.TabularInline):
    model = models.DiscussionRecipient


class DiscussionHeadAdmin(admin.ModelAdmin):
    inlines = [DiscussionInline, DiscussionUserGroupInline]


class DiscussionAdmin(admin.ModelAdmin):
    search_fields = ['message', 'created_at']
    list_display = ['message', 'created_at']


class DiscussionUserGroupAdmin(admin.ModelAdmin):
    pass


class DiscussionRecipientAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.DiscussionHead, DiscussionHeadAdmin)
admin.site.register(models.Discussion, DiscussionAdmin)
admin.site.register(models.DiscussionUserGroup, DiscussionUserGroupAdmin)
admin.site.register(models.DiscussionRecipient, DiscussionRecipientAdmin)