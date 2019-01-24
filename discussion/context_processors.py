from . import models
from friends.models import Friend
from . import forms
from django.db.models import Q
from django.shortcuts import render, HttpResponse


def discussion_notification(request):
    user_friends = Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)) &
                                                Q(friendship_status=1)).all()
    friends_list = [request.user.id]
    for user_friend in user_friends:
        if user_friend.user_one_id == request.user.id:
            friends_list.append(user_friend.user_two_id)
        else:
            friends_list.append(user_friend.user_one_id)
    # return HttpResponse(user_friends)
    heads = models.DiscussionHead.objects.filter(created_by_id__in=friends_list).distinct('id').order_by('id', 'messages__created_at')
    count = 0
    for head in heads:
        temp = models.DiscussionRecipient.objects.filter(Q(discussion_head_id=head.id) & Q(recipient_id=request.user.id) & Q(is_read=False)).count()
        head.unread_count = temp
        count += temp

    return {
        'discussion_heads': heads,
        'unread_discussion': count
    }


def discussion_head_create_form(request):
    discussion_head_form = forms.DiscussionHeadForm()
    return {'discussion_head_form': discussion_head_form}
