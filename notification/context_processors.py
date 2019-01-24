from . import models


def user_notification(request):
    return {'notifications': models.Notification.objects.filter(to_user_id=request.user.id).order_by('-created_at'),
            'cout_not_read_notification':  models.Notification.objects.filter(to_user_id=request.user.id,
                                                                              post_status=False)}
