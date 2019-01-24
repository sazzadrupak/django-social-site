from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index, name='notification'),
    path('ajax/notification_status_change', views.notification_status_change, name='notification_status_change'),
    path('get_all_notification_info', views.get_all_notification_info, name='get_all_notification_info')
]
urlpatterns += staticfiles_urlpatterns()
