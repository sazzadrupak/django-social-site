from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bwa2018djangoproject import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='discussion'),
    path('create_new_discussion', views.create_new_discussion, name='create_new_discussion'),
    path('all_discussions', views.all_discussions, name='see_all_discussion'),
    path('get_discussion_head_texts/<slug:discussion_head_id>', views.get_discussion_head_texts,
         name='get_discussion_head_texts'),
    path('save_chat', views.save_chat, name='save_chat'),
    path('discussion_head_view_update', views.discussion_head_view_update, name='discussion_head_view_update'),
    path('add_chat_after_view/<slug:discussion_head_id>', views.add_chat_after_view, name='add_chat_after_view'),
    path('discussion_head_lists_update/<slug:discussion_head_id>', views.discussion_head_lists_update, name='discussion_head_lists_update'),
    path('message/<slug:discussion_head_id>', views.message, name='message'),
    path('all_discussion_search_result', views.all_discussion_search_result, name='all_discussion_search_result'),
    path('single_discussion_search_result', views.single_discussion_search_result, name='single_discussion_search_result'),
    path('get_discussion_info', views.get_discussion_info, name='get_discussion_info'),
    path('get_message/<slug:chat_id>', views.get_message, name='get_message'),
    path('chat_update', views.chat_update, name='chat_update'),
    path('cancel_message_edit/<slug:chat_id>/<slug:head_id>', views.cancel_message_edit, name='cancel_message_edit'),
    path('delete_chat/<slug:chat_id>', views.delete_chat, name="delete_chat"),
    path('delete_discussion_head/<slug:discussion_head_id>', views.delete_discussion_head, name='delete_discussion_head')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
