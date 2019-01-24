from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from . import forms
from . import models

from django.db.models import Q
from django.contrib.auth.models import User
from friends.models import Friend

from notification.models import Notification
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
# Create your views here.


@login_required(login_url='login')
def index(request):
    if request.user.is_authenticated:
        status_text_form = forms.StatusTextForm()
        comment_text_form = forms.CommentTextForm()
        offset = 0
        limit = 5
        friends = Friend.objects.filter((~Q(user_one_id=request.user.id) | ~Q(user_two_id=request.user.id))
                                        & Q(friendship_status=1)).all()

        friends_id = [request.user.id]
        for friend in friends:
            if request.user.id == friend.user_one_id:
                friends_id.append(friend.user_two_id)
            elif request.user.id == friend.user_two_id:
                friends_id.append(friend.user_one_id)
            else:
                pass
        posts = available_status_result(offset, limit, friends_id)
        page_name = 'Home'
        other_users = friend_request_not_send_yet_users(request.user.id)  # list of user to whom friend request hasn't been sent yet
        # return HttpResponse(other_users)
        if request.method == 'POST':
            status_text_form = forms.StatusTextForm(request.POST)
            if status_text_form.is_valid():
                status_message = models.Post()
                status_message.post_text = status_text_form.data['status_text']
                status_message.post_status = True
                status_message.user_id = request.user.id
                status_message.save()

                # send friends notification about post add
                post_id = models.Post.objects.filter(user_id=request.user.id).latest('id')

                for friend_id in friends_id:
                    current_site = get_current_site(request)
                    comment_notification = Notification()
                    comment_notification.from_user_id = request.user.id
                    comment_notification.to_user_id = friend_id
                    comment_notification.notification_text = '<a href="' \
                                                             'https://' + current_site.domain + '/status_details/' + \
                                                             str(post_id.pk) + '">' \
                                                             + request.user.first_name + ' ' + request.user.last_name + ' added a post.</a>'
                    if friend_id == request.user.id:
                        pass
                    else:
                        comment_notification.save()

                return redirect('/')
        # post = models.Post.objects.get(id=1)
        # return HttpResponse(post.comments.all())
        if posts.count() > 0:
            last_item_id = posts[posts.count() - 1].id
        else:
            last_item_id = 0
            
        return render(request, 'home/home.html', {'page_name': page_name, 'status_text_form': status_text_form,
                                                  'posts': posts, 'comment_text_form': comment_text_form,
                                                  'last_item_id': last_item_id, 'other_users': other_users
                                                  })
    else:
        return redirect('login/')


def available_status_result(offset, limit, friends_id):
    # get 5 status texts every time which are active and order by created_at
    # also excluded those status texts which are already shown in template page, and get other 5 status texts
    return models.Post.objects.filter(post_status=True, user_id__in=friends_id).order_by('-created_at')
    # return models.Post.objects.filter(post_status=True).order_by('-created_at')[offset: limit]


def friend_request_not_send_yet_users(user_id):
    user_in_friend_table = Friend.objects.filter(Q(user_one_id=user_id) | Q(user_two_id=user_id)).values('user_one_id', 'user_two_id')
    user_id_list = []
    for u in user_in_friend_table:
        if u['user_one_id'] not in user_id_list:
            user_id_list.append(u['user_one_id'])

        if u['user_two_id'] not in user_id_list:
            user_id_list.append(u['user_two_id'])
    user_id_list.append(user_id)
    return User.objects.exclude(id__in=user_id_list).filter(~Q(is_superuser=True) & Q(is_active=True))


@login_required(login_url='/')
def comment_add(request):
    '''
    Add a comment to a post
    :param request:
    :return:
    '''
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment_add_form = forms.CommentTextForm(request.POST)
            if comment_add_form.is_valid():
                comment_text_add = models.Comment()
                comment_text_add.comment_text = comment_add_form.data['comment_text']
                comment_text_add.post_id = request.POST['post_id']
                comment_text_add.user_id = request.user.id
                comment_text_add.save()

                comments = models.Comment.objects.filter(post_id=comment_text_add.post_id)

                post_info = models.Post.objects.get(id=request.POST['post_id'])
                if post_info.user_id == request.user.id:
                    pass
                else:
                    current_site = get_current_site(request)
                    comment_notification = Notification()
                    comment_notification.from_user_id = request.user.id
                    comment_notification.to_user_id = post_info.user_id
                    comment_notification.notification_text = '<a href="' \
                                                             'https://'+current_site.domain+'/status_details/' +\
                                                             request.POST['post_id']+'">'\
                                                             + request.user.username+' commented on your status.</a>'
                    comment_notification.save()
                return render(request, 'home/comments.html', {'comments': comments})
    else:
        return redirect('login/')


def more_status_after_mouse_scroll(request, last_item_id):
    if request.user.is_authenticated:
        offset = 5
        limit = 5

        posts = available_status_result(offset, limit)
        print(posts.query)
        comment_text_form = forms.CommentTextForm()
        if len(posts) > 0:
            last_item_id = posts[len(posts) - 1].id
        else:
            last_item_id = 0
        return render(request, 'home/more_status_after_mouse_scroll.html', {'posts': posts,
                                                                            'comment_text_form': comment_text_form,
                                                                            'last_item_id': last_item_id})
    else:
        return redirect('login/')


@login_required(login_url='/')
def status_details(request, post_id):
    try:
        post_info = models.Post.objects.get(id=post_id)

        # check if the user who post the status and the user who are trying to read the post are friends
        friendship_info = Friend.objects.filter((Q(user_one_id=request.user.id) & Q(user_two_id=post_info.user_id)) |
                                                (Q(user_one_id=post_info.user_id) & Q(user_two_id=request.user.id))
                                                & Q(friendship_status=1))
        if request.user.id == post_info.user_id or len(friendship_info) > 0:
            comment_text_form = forms.CommentTextForm()
            page_name = 'Status details'
            return render(request, 'home/status_details.html', {'post': post_info, 'page_name': page_name,
                                                                'comment_text_form': comment_text_form})
        else:
            messages.error(request, 'You do not have rights to read other user post. First create a friendship')
            return HttpResponseRedirect('/')
    except models.Post.DoesNotExist:
        messages.error(request, 'No post found.')
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def edit_post(request, post_id):
    '''
    edit a post
    :param request:
    :param post_id:
    :return:
    '''
    check_status_by_valid_user = models.Post.objects.get(user_id=request.user.id, id=post_id)

    try:
        status_text_form = forms.StatusTextForm(initial={'status_text': check_status_by_valid_user.post_text})
        if request.method == 'POST':
            status_text_form = forms.StatusTextForm(request.POST)
            if status_text_form.is_valid():
                status_message = models.Post.objects.get(user_id=request.user.id, id=post_id)
                status_message.post_text = status_text_form.data['status_text']
                status_message.save()
                return HttpResponseRedirect('/status_details/'+post_id)
        return render(request, 'home/edit_post.html', {'page_name': 'Edit post', 'status_text_form': status_text_form})
    except models.Post.DoesNotExist:
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def delete_post(request, post_id):
    '''
    Delete a post and also it's associate comments
    :param request:
    :param post_id:
    :return:
    '''
    check_status_by_valid_user = models.Post.objects.get(user_id=request.user.id, id=post_id)

    try:
        associated_comments = models.Comment.objects.filter(user_id=request.user.id, id=post_id)

        if len(associated_comments) > 0:
            for associated_comment in associated_comments:
                associated_comment.delete()

        check_status_by_valid_user.delete()

        messages.success(request, "Post deleted successfully.")
        return HttpResponseRedirect('/')

    except models.Post.DoesNotExist:
        messages.error(request, "The post you are trying to delete, is not your post.")
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def get_comment(request, comment_id):
    comment = models.Comment.objects.get(id=comment_id)
    comment_text_form = forms.CommentTextForm(initial={'comment_text': comment.comment_text})
    return render(request, 'home/edit_comment.html', {'comment_text_form': comment_text_form, 'comment_id': comment_id,
                                                      'post_id': comment.post.id})


@login_required(login_url='/')
def cancel_comment_edit(request, comment_id, post_id):
    '''
    pass the comment text to template when user cancel edit comment
    :param request:
    :param comment_id:
    :param post_id:
    :return:
    '''
    try:
        comment = models.Comment.objects.get(post_id=post_id, user_id=request.user.id, id=comment_id)
        return HttpResponse(comment.comment_text)
    except models.Comment.DoesNotExist:
        messages.error(request, "The comment you are trying to update, is not your comment.")
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def comment_update(request):
    '''
    update the comment and pass the updated text to the template
    :param request:
    :return:
    '''
    try:
        comment = models.Comment.objects.get(post_id=request.POST['post_id'], user_id=request.user.id, id=request.POST['comment_id'])
        comment_update_form = forms.CommentTextForm(request.POST)
        if comment_update_form.is_valid():
            comment.comment_text = comment_update_form.data['comment_text']
            comment.save()
            return HttpResponse(comment_update_form.data['comment_text'])
    except models.Comment.DoesNotExist:
        messages.error(request, "The comment you are trying to update, is not your comment.")
        return HttpResponseRedirect('/')


@login_required(login_url='/')
def delete_comment(request, comment_id, post_id):
    '''
    delete a comment
    :param request:
    :param comment_id:
    :param post_id:
    :return:
    '''

    try:
        comment = models.Comment.objects.get(post_id=post_id, id=comment_id)
        comment.delete()
        return JsonResponse({'post_status': True})
    except models.Comment.DoesNotExist:
        messages.error(request, "The comment you are trying to update, is not your comment.")
        return HttpResponseRedirect('/')
