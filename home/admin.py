from django.contrib import admin

# Register your models here.
from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, ]
    search_fields = ['post_text', 'user', 'post_status', 'created_at']
    list_display = ['post_text', 'user', 'post_status', 'created_at']


class CommentAdmin(admin.ModelAdmin):
    search_fields = ['comment_text', 'user', 'created_at']
    list_display = ['comment_text', 'user', 'created_at']


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
