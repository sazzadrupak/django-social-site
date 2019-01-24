from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from notification.models import Notification
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.


@login_required(login_url='/')
def friend_list(request):
    '''
    This view shows the user friend list, from whom user got friend request, and to whom user gave friend request
    :param request:
    :return:
    '''
    if request.user.is_authenticated:
        page_name = 'Friends'
        friends = models.Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)) &
                                               Q(friendship_status=1)).all()

        requested = models.Friend.objects.filter((Q(user_one_id=request.user.id) & Q(lead_user_id=request.user.id)) &
                                                 Q(friendship_status=0)).all()

        request_lists = models.Friend.objects.filter((Q(user_two_id=request.user.id) & ~Q(lead_user_id=request.user.id))
                                                     & Q(friendship_status=0)).all()
        # return HttpResponse(User.objects.get(id=requested[0].user_two_id))
        return render(request, 'friends/friend_list.html', {'page_name': page_name, 'requested': requested,
                                                            'request_lists': request_lists, 'friends': friends})


@login_required(login_url='/')
def create_friendship(request):
    '''
    Send a friend ship request to a users
    :param request:
    :return:
    '''
    friend_request_send_form = forms.FriendRequestSendForm(request.POST)
    if friend_request_send_form.is_valid():
        friend_request = models.Friend()
        friend_request.user_one_id = friend_request_send_form.data['user_one_id']
        friend_request.user_two_id = friend_request_send_form.data['user_two_id']
        friend_request.lead_user_id = request.user.id  # friend_request_send_form.data['lead_user_id']
        friend_request.save()
        request_to_user = User.objects.get(id=friend_request.user_two_id)
        messages.success(request, "A friend request has been sent to {}".format(request_to_user.username))

        current_site = get_current_site(request)
        comment_notification = Notification()
        comment_notification.from_user_id = request.user.id
        comment_notification.to_user_id = friend_request.user_two_id
        comment_notification.notification_text = '<a href="https://' + current_site.domain + '/friends">' \
                                                 + request.user.first_name + ' ' + request.user.last_name \
                                                 + ' sent you a friend request.</a>'
        comment_notification.save()
    else:
        messages.error(request, "Friend request can not be sent right now. Try again later.")
    return HttpResponseRedirect('/')


@login_required(login_url='/')
def delete_friendship_request(request):
    '''
    delete a friendship between two users
    :param request:
    :return:
    '''

    comment_notification = Notification()
    notification_message = ''

    request_info = models.Friend.objects.get(id=request.POST['request_id'])
    # decline a friend request from other user
    if request.POST['friendship_status'] == '2':

        messages.success(request, "{}'s Request has been declined".format(request_info.user_one.username))
        notification_message = "{} declined your request".format(request.user.first_name+' '+request.user.last_name)
        comment_notification.from_user_id = request.user.id
        comment_notification.to_user_id = request_info.user_one_id

    # remove a request sent to another user
    elif request.POST['friendship_status'] == '3':

        messages.success(request, "You have deleted the request sent to {}".format(request_info.user_two.username))
        comment_notification.from_user_id = request.user.id
        comment_notification.to_user_id = request_info.user_two_id
        notification_message = "{} withdraw the request sent to you".format(request.user.first_name+' '+request.user.last_name)

    # delete a friendship
    elif request.POST['friendship_status'] == '4':
        # if logged in user id is same as user_one_id, then logged in user trying to delete friendship with user_one_id
        if request.user.id == request_info.user_one_id:

            messages.success(request, "You have deleted the friendship with {}".format(request_info.user_two.username))
            comment_notification.from_user_id = request.user.id
            comment_notification.to_user_id = request_info.user_two_id

        # if logged in user id is same as user_two_id, then logged in user trying to delete friendship with user_one_id
        else:

            messages.success(request, "You have deleted the friendship with {}".format(request_info.user_one.username))
            comment_notification.from_user_id = request.user.id
            comment_notification.to_user_id = request_info.user_one_id

        notification_message = "{} have deleted the friendship with you".format(request.user.first_name+' '+request.user.last_name)

    request_info.delete()

    comment_notification.notification_text = notification_message
    comment_notification.save()

    return HttpResponseRedirect('/friends')


@login_required(login_url='/')
def accept_friendship_request(request):
    '''
    Accept an friend request
    :param request:
    :return:
    '''
    request_accept = models.Friend.objects.get(id=request.POST['request_id'])
    request_accept.friendship_status = 1
    request_accept.save()

    messages.success(request, "You are now friend with {}".format(request_accept.user_one.username))

    current_site = get_current_site(request)
    comment_notification = Notification()
    comment_notification.from_user_id = request.user.id
    comment_notification.to_user_id = request_accept.user_one_id
    comment_notification.notification_text = '<a href="https://' + current_site.domain + '/friends">' \
                                             + request.user.first_name + ' ' + request.user.last_name \
                                             + ' accepted your friend request.</a>'
    comment_notification.save()

    return HttpResponseRedirect('/friends')
