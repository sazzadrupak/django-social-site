from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from . import models
from . import forms
from django.db.models import Q
from notification.models import Notification
from friends.models import Friend
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
# Create your views here.


def index():
    pass


def create_new_discussion(request):
    '''
    all discussion head list view
    :param request:
    :return:
    '''
    friends_list = [request.user.id]
    new_discussion_form = forms.DiscussionHeadForm(request.POST)
    if new_discussion_form.is_valid():
        discussion_head = models.DiscussionHead()
        discussion_head.created_by_id = request.user.id
        discussion_head.head_name = request.POST['head_name']
        discussion_head.save()

        head_id = models.DiscussionHead.objects.filter(created_by_id=request.user.id).latest('id')
        last_head_id = head_id.pk

        user_friends = Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)) &
                                             Q(friendship_status=1)).all()

        if len(user_friends) > 0:
            comment_notification = Notification()
            comment_notification.from_user_id = request.user.id

            for user_friend in user_friends:
                if user_friend.user_one_id == request.user.id:
                    comment_notification.to_user_id = user_friend.user_two_id
                    friends_list.append(user_friend.user_two_id)
                else:
                    comment_notification.to_user_id = user_friend.user_one_id
                    friends_list.append(user_friend.user_one_id)
            sender_name = request.user.first_name+' '+request.user.last_name
            current_site = get_current_site(request)
            comment_notification.notification_text = '<a href="https://'+current_site.domain+'/discussion/message/' + \
                                                     str(last_head_id) + '">'+sender_name+' created a discussion group.</a>'
            comment_notification.save()

    heads = models.DiscussionHead.objects.filter(created_by_id__in=friends_list).distinct('id').order_by('id', 'messages__created_at')

    return render(request, 'discussion/discussion_form.html', {'discussion_head_form': new_discussion_form,
                                                               'discussion_heads': heads})


@login_required(login_url='login')
def all_discussions(request):
    '''
    Show all discussion head in templates
    :param request:
    :return:
    '''
    page_name = 'All discussion'
    try:
        discussion_head = models.DiscussionHead.objects.order_by('messages__created_at').values('id')
        if len(discussion_head) > 0:
            discussion_head = discussion_head[0]['id']
    except models.DiscussionHead.DoesNotExist:
        discussion_head = 0
    # return HttpResponse(discussion_head)
    discussion_form = forms.DiscussionForm(initial={'discussion_head_id': discussion_head})
    return render(request, 'discussion/all_discussion.html', {'page_name': page_name, 'discussion_form': discussion_form})


@login_required(login_url='login')
def get_discussion_head_texts(request, discussion_head_id):
    '''
    Show a specific discussion heads' messages
    :param request:
    :param discussion_head_id:
    :return:
    '''
    discussion_form = forms.DiscussionForm(initial={'discussion_head_id': discussion_head_id})
    chats = models.Discussion.objects.filter(discussion_head_id=discussion_head_id)
    return render(request, 'discussion/discussion_head_chats.html', {'chats': chats, 'discussion_form': discussion_form,
                                                                     'discussion_head_id': discussion_head_id})


@login_required(login_url='login')
def save_chat(request):
    '''
    Save a text message and send notification to those user who already have sent message in this specific discussion head
    :param request:
    :return:
    '''
    message_form = forms.DiscussionForm(request.POST)
    if message_form.is_valid():
        message_data = models.Discussion()
        message_data.message = message_form.cleaned_data['message']
        message_data.sender_id = request.user.id
        message_data.discussion_head_id = message_form.cleaned_data['discussion_head_id']
        message_data.save()

        message_id = models.Discussion.objects.filter(sender_id=request.user.id).latest('id')
        last_message_id = message_id.pk
        # check if current user is in the discussion head group
        if len(models.DiscussionUserGroup.objects.filter(Q(discussion_user_id=request.user.id) & Q(discussion_head_id=message_form.cleaned_data['discussion_head_id'])).all()) > 0:
            pass
        else:
            # add current user to the discussion user group
            user_group = models.DiscussionUserGroup()
            user_group.discussion_head_id = message_form.cleaned_data['discussion_head_id']
            user_group.discussion_user_id = request.user.id
            user_group.save()

        # get the list of discussion user groups
        discussion_users = models.DiscussionUserGroup.objects.filter(discussion_head_id=message_form.cleaned_data['discussion_head_id'])

        temp = []
        if len(discussion_users) > 0:  # check if discussion head has user groups
            for discussion_user in discussion_users:
                if discussion_user.discussion_user_id == request.user.id:
                    is_read = True
                else:
                    is_read = False

                temp = [
                    models.DiscussionRecipient(
                        is_read=is_read,
                        recipient_id=discussion_user.discussion_user_id,
                        discussion_head_id=message_form.cleaned_data['discussion_head_id'],
                        discussion_id=last_message_id
                    )
                ]
                models.DiscussionRecipient.objects.bulk_create(temp)
        # return HttpResponse(temp)
        else:
            discussion_recipient_object = models.DiscussionRecipient()
            discussion_recipient_object.is_read = True
            discussion_recipient_object.recipient_id = request.user.id
            discussion_recipient_object.discussion_id = message_id.pk
            discussion_recipient_object.save()
        return HttpResponse(1)

    return HttpResponse(0)


@login_required(login_url='login')
def discussion_head_view_update(request):
    '''
    Update discussion head to show if a new text message added to it every after 5 seconds
    :param request:
    :return:
    '''
    chats = ''
    discussion_head_id = 0
    try:
        user_friends = Friend.objects.filter((~Q(user_one_id=request.user.id) | ~Q(user_two_id=request.user.id)) &
                                             Q(friendship_status=1)).all()
        friends_list = [request.user.id]
        for user_friend in user_friends:
            if user_friend.user_one_id == request.user.id:
                friends_list.append(user_friend.user_two_id)
            else:
                friends_list.append(user_friend.user_one_id)

        discussion_head = models.DiscussionHead.objects.filter(created_by_id__in=friends_list).distinct('id').order_by(
            'id', 'messages__created_at').values('id')
        if len(discussion_head) > 0:
            discussion_head_id = discussion_head[0]['id']
            chats = models.Discussion.objects.filter(discussion_head_id=discussion_head_id)
    except models.DiscussionHead.DoesNotExist:
        discussion_head_id = 0
    discussion_form = forms.DiscussionForm(initial={'discussion_head_id': discussion_head_id})
    return render(request, 'discussion/all_discussion_update_view.html', {'discussion_form': discussion_form,
                                                                          'discussion_head_id': discussion_head_id,
                                                                          'chats': chats,
                                                                          })


@login_required(login_url='login')
def add_chat_after_view(request, discussion_head_id):
    '''
    Show text messages of a discussion head in template every after 5 seconds
    :param request:
    :param discussion_head_id:
    :return:
    '''

    try:
        chat_recipients = models.DiscussionRecipient.objects.filter(Q(discussion_head_id=discussion_head_id) & Q(recipient_id=request.user.id))
        if len(chat_recipients) > 0:
            for chat in chat_recipients:
                chat_update = models.DiscussionRecipient()
                chat_update.id = chat.id
                chat_update.discussion_id = chat.discussion_id
                chat_update.is_read = True
                chat_update.discussion_head_id = discussion_head_id
                chat_update.recipient_id = request.user.id
                chat_update.save()
    except models.DiscussionRecipient.DoesNotExist:
        pass
    chats = models.Discussion.objects.filter(discussion_head_id=discussion_head_id)
    return render(request, 'discussion/add_chat_after_view.html', {'discussion_head_id': discussion_head_id,
                                                                   'chats': chats})


@login_required(login_url='login')
def discussion_head_lists_update(request, discussion_head_id):
    '''
    Update discussion head lists of the menu bar to show user notification of new text messages after every 15 seconds
    :param request:
    :param discussion_head_id:
    :return:
    '''
    try:
        chats = models.DiscussionRecipient.objects.filter(Q(discussion_head_id=discussion_head_id) & Q(recipient_id=request.user.id))
        if len(chats) > 0:
            for chat in chats:
                chat_update = models.DiscussionRecipient()
                chat_update.id = chat.id
                chat_update.discussion_id = chat.discussion_id
                chat_update.is_read = True
                chat_update.discussion_head_id = discussion_head_id
                chat_update.recipient_id = request.user.id
                chat_update.save()
    except models.DiscussionRecipient.DoesNotExist:
        pass

    return render(request, 'discussion/discussion_head_lists_update.html', {'discussion_head_id': discussion_head_id})


@login_required(login_url='login')
def message(request, discussion_head_id):
    '''
    get the individual discussion view
    :param request:
    :param discussion_head_id:
    :return:
    '''
    try:
        discussion_head = models.DiscussionHead.objects.filter(id=discussion_head_id)
        if len(discussion_head) > 0:
            page_name = discussion_head[0].head_name
            chats = models.DiscussionRecipient.objects.filter(
                Q(discussion_head_id=discussion_head_id) & Q(recipient_id=request.user.id))
            if len(chats) > 0:
                for chat in chats:
                    chat_update = models.DiscussionRecipient()
                    chat_update.id = chat.id
                    chat_update.discussion_id = chat.discussion_id
                    chat_update.is_read = True
                    chat_update.discussion_head_id = discussion_head_id
                    chat_update.recipient_id = request.user.id
                    chat_update.save()

            messages = models.Discussion.objects.filter(discussion_head_id=discussion_head_id)
            discussion_form = forms.DiscussionForm(initial={'discussion_head_id': discussion_head_id})
            return render(request, 'discussion/message.html', {'chats': messages, 'discussion_head_id': discussion_head_id,
                                                               'page_name': page_name, 'discussion_form': discussion_form})
        else:
            return render(request, 'discussion/discussion_not_found.html', {})
    except models.DiscussionHead.DoesNotExist:
        return render(request, 'discussion/discussion_not_found.html', {})


@login_required(login_url='login')
def all_discussion_search_result(request):
    '''
    Search discussions using user name and text value
    :param request:
    :return:
    '''
    chats = ''
    # user name search
    users = User.objects.filter(Q(is_superuser=False) & (Q(username__iregex=request.POST['search_value']) |
                                       Q(first_name__iregex=request.POST['search_value']) |
                                       Q(last_name__iregex=request.POST['search_value']))).distinct('id').values('id')
    # return HttpResponse(users)

    user_list = list()
    if len(users) > 0:
        for single_user in users:
            user_friends = Friend.objects.filter(((Q(user_one_id=request.user.id) & Q(user_two_id=single_user['id'])) |
                                                 (Q(user_one_id=single_user['id']) & Q(user_two_id=request.user.id))) &
                                                Q(friendship_status=1))
            if len(user_friends) > 0:
                for user_friend in user_friends:
                    if user_friend.user_one_id == request.user.id:
                        user_list.append(user_friend.user_two_id)
                    elif user_friend.user_two_id == request.user.id:
                        user_list.append(user_friend.user_one_id)

        chats = models.DiscussionHead.objects.filter(head_users__discussion_user_id__in=user_list).distinct('id')\
            .order_by('id', 'messages__created_at')
        return render(request, 'discussion/discussion_username_search.html', {'discussion_heads': chats})
    # chat text search
    if len(chats) == 0:
        message_list = list()
        messages = models.Discussion.objects.filter(message__iregex=request.POST['search_value'])
        # return HttpResponse(messages)
        if len(messages) > 0:
            for message in messages:
                check_user_group = models.DiscussionUserGroup.objects.filter(
                    Q(discussion_head_id=message.discussion_head_id) & Q(discussion_user_id=request.user.id))
                if len(check_user_group) > 0:
                    message_list.append(message)
        return render(request, 'discussion/discussion_text_search.html', {'discussion_heads': message_list})


@login_required(login_url='login')
def single_discussion_search_result(request):
    '''
    search text inside a discussion
    :param request:
    :return:
    '''
    messages = models.Discussion.objects.filter(Q(message__iregex=request.POST['search_value']) &
                                                Q(discussion_head_id=request.POST['discussion_head_id']))
    return render(request, 'discussion/single_discussion_search_result.html', {'chats': messages, 'discussion_head_id':
        request.POST['discussion_head_id']})


def get_discussion_info(request):
    '''
    get the discussion info to notify user after every 15 seconds
    :param request:
    :return:
    '''
    return render(request, 'discussion/check_discussion_ajax.html', {})


@login_required(login_url='login')
def get_message(request, chat_id):
    '''
    get the message text
    :param request:
    :param chat_id:
    :return:
    '''

    message_text = models.Discussion.objects.get(id=chat_id)
    message_text_form = forms.DiscussionForm(initial={'message': message_text.message, 'discussion_head_id': message_text.discussion_head.id })
    return render(request, 'discussion/edit_message.html', {'message_text_form': message_text_form, 'chat_id': chat_id, 'head_id': message_text.discussion_head.id })


@login_required(login_url='login')
def chat_update(request):
    '''
    update a message text
    :param request:
    :return:
    '''
    try:
        message_text = models.Discussion.objects.get(discussion_head_id=request.POST['discussion_head_id'], sender_id=request.user.id, id=request.POST['chat_id'])
        message_update_form = forms.DiscussionForm(request.POST)
        if message_update_form.is_valid():
            message_text.message = message_update_form.data['message']
            message_text.save()
            return HttpResponse(message_update_form.data['message'])
    except models.Discussion.DoesNotExist:
        messages.error(request, "The message you are trying to update, is not your message.")
        return HttpResponseRedirect('/')


@login_required(login_url='login')
def cancel_message_edit(request, chat_id, head_id):
    '''
    cancel an message text edit event and return the previous text
    :param request:
    :param chat_id:
    :param head_id:
    :return:
    '''

    try:
        message_info = models.Discussion.objects.get(discussion_head_id=head_id, id=chat_id, sender_id=request.user.id)
        return HttpResponse(message_info.message)
    except models.Discussion.DoesNotExist:
        messages.error(request, "The message you are trying to update, is not your message.")
        return HttpResponseRedirect('/')


@login_required(login_url='login')
def delete_chat(request, chat_id):
    '''
    delete a message text
    :param request:
    :param chat_id:
    :return:
    '''
    try:
        message_text = models.Discussion.objects.get(sender_id=request.user.id, id=chat_id)
        message_text.delete()
        return JsonResponse({'post_status': True})
    except models.Discussion.DoesNotExist:
        messages.error(request, "The message you are trying to update, is not your message.")
        return HttpResponseRedirect('/')


@login_required(login_url='login')
def delete_discussion_head(request, discussion_head_id):
    '''
    delete a head and associated user group, recipients and text messages
    :param request:
    :param discussion_head_id:
    :return:
    '''

    try:
        check_head_authentication = models.DiscussionHead.objects.filter(id=discussion_head_id, created_by_id=request.user.id)
        if len(check_head_authentication) > 0:
            recipient_delete = models.DiscussionRecipient.objects.filter(discussion_head_id=discussion_head_id).delete()
            user_group_delete = models.DiscussionUserGroup.objects.filter(discussion_head_id=discussion_head_id).delete()
            discussion_delete = models.Discussion.objects.filter(discussion_head_id=discussion_head_id).delete()
            discussion_delete = models.DiscussionHead.objects.filter(id=discussion_head_id).delete()
            return HttpResponseRedirect('/profile')

    except models.DiscussionHead.DoesNotExist:
        messages.error(request, "The discussion head you are trying to update, is not yours.")
        return HttpResponseRedirect('/')
