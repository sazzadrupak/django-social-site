"""bwa2018djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from bwa2018djangoproject import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.profile, name='profile'),
    path(r'edit/', views.edit_profile, name='edit_profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('upload_profile_image', views.upload_profile_image, name='upload_profile_image'),
    path('delete_account', views.delete_account, name='delete_account'),
    # path('other/<slug:username1>.+', views.user_profile, name='other'),
    re_path(r'^other/(?P<username1>.*)/$', views.user_profile, name='other'),
    re_path(r'^user_search/$', views.user_search, name='user_search'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
