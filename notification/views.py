from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from . import models
# Create your views here.


def index():
    pass


def notification_status_change(request):
    notification = models.Notification.objects.filter(to_user_id=request.user.id).update(post_status=True)
    return JsonResponse({'post_status': True})


def get_all_notification_info(request):
    return render(request, 'notification/check_notification_ajax.html', {})
