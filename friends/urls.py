
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from bwa2018djangoproject import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.friend_list, name='friend_list'),
    path('create_friendship', views.create_friendship, name='create_friendship'),
    path('delete_friendship_request', views.delete_friendship_request, name='delete_friendship_request'),
    path('accept_friendship_request', views.accept_friendship_request, name='accept_friendship_request')
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
