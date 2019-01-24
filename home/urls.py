from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bwa2018djangoproject import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path('comment_add/', views.comment_add, name='comment_add'),
    path('more_status_after_mouse_scroll/<slug:last_item_id>', views.more_status_after_mouse_scroll,
         name='more_status_after_mouse_scroll'),
    path('status_details/<slug:post_id>', views.status_details,
         name='status'),
    path('edit_post/<slug:post_id>', views.edit_post, name='edit_post'),
    path('delete_post/<slug:post_id>', views.delete_post, name='delete_post'),
    path('get_comment/<slug:comment_id>', views.get_comment, name='get_comment'),
    path('delete_comment/<slug:comment_id>/<slug:post_id>', views.delete_comment, name='delete_comment'),
    path('cancel_comment_edit/<slug:comment_id>/<slug:post_id>', views.cancel_comment_edit, name='cancel_comment_edit'),
    path('comment_update', views.comment_update, name="comment_update")
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
