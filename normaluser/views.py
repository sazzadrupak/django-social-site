from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
# from django.db import connection
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages

from _datetime import datetime
from . import forms
from . import models
from home.models import Post, Comment
from friends.models import Friend
from notification.models import Notification
from discussion.models import DiscussionHead, Discussion, DiscussionRecipient, DiscussionUserGroup
from django.contrib.auth.models import User
from django.db.models import Q
import hashlib


# login templates, authenticate and login a user
def user_login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user_object = models.User.objects.get(email=email)
            user = authenticate(username=user_object.username, password=password)
            login(request, user)
            # messages.success(request, "Your account has been activated successfully. Now you can login.")
            return redirect('/')

    else:
        login_form = forms.LoginForm()

    return render(request, 'login/login.html', {'login_form': login_form})


def computeMD5Hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def user_registration(request):
    now = datetime.now()

    user_form = forms.RegistrationForm()
    profile_form = forms.UserProfileInfoForm({'gender': 'm'})
    if request.method == 'POST':
        user_form = forms.RegistrationForm(request.POST)
        profile_form = forms.UserProfileInfoForm(request.POST)
        if user_form.is_valid():

            user_object = models.User()
            user_object.first_name = user_form.data['first_name']
            user_object.last_name = user_form.data['last_name']
            user_object.username = user_form.data['username']
            user_object.email = user_form.data['email']
            user_object.password = make_password(user_form.data['password'])
            user_object.is_active = False
            user_object.save()

            profile_object = models.NormalUser()

            year = 1970
            if request.POST['year'] != '':
                year = request.POST['year']

            month = 12
            if request.POST['month'] != '':
                month = request.POST['month']

            day = 12
            if request.POST['day'] != '':
                day = request.POST['day']

            profile_object.birth_date = datetime.strptime(str(year)+'-'+str(month)+'-'+str(day), "%Y-%m-%d").date()
            profile_object.address = profile_form.data['address']
            profile_object.phone_number = profile_form.data['phone_number']
            profile_object.gender = profile_form.data['gender']
            profile_object.user_id = user_object.id
            profile_object.email_validation_code = computeMD5Hash(user_object.username)

            profile_object.save()
            current_site = get_current_site(request)

            html_content = render_to_string('registration/email_authentication.html',
                                            {'email_authentication_code': profile_object.email_validation_code,
                                             'first_name': user_object.first_name,
                                             'last_name': user_object.last_name, 'domain': current_site.domain})
            text_content = strip_tags(html_content)

            connection = mail.get_connection()
            connection.open()
            email1 = mail.EmailMessage(
                'Confirm your account on Social site',
                text_content,
                'sazzad.rupak17@gmail.com',
                [user_object.email],
                connection=connection
            )
            email1.send()
            connection.close()

            return render(request, 'registration/email_sent_message.html', {
                'email_authentication_code': profile_object.email_validation_code, 'first_name': user_object.first_name,
                'last_name': user_object.last_name})
        else:
            return render(request, 'registration/registration.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        return render(request, 'registration/registration.html', {'user_form': user_form, 'profile_form': profile_form,
                                                                  'days': range(1, 32, 1), 'months': range(1, 13, 1),
                                                                  'years': range(now.year, 1970, -1)})


# Check if an email id is unique or not
def check_uniqe_email_id(request):
    email = request.GET.get('email_id')

    match = models.User.objects.filter(email=email).exists()
    # print(connection.queries)
    return JsonResponse({'is_taken': match}, safe=False)


# activate an account by clicking the activation link
def email_authenticate_registration(request, email_validation_code):
    p = models.NormalUser.objects.get(email_validation_code=email_validation_code)
    user_object = models.User.objects.get(id=p.user.id)
    user_object.is_active = True
    user_object.save()

    p.email_validation_code = ''
    p.save()
    messages.success(request, "Your account has been activated successfully. Now you can login.")
    return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return redirect('login/')


def user_password_reset(request):
    reset_form = forms.UserPasswordResetForm()
    if request.method == 'POST':
        reset_form = forms.UserPasswordResetForm(request.POST)
        if reset_form.is_valid():
            email = reset_form.data['email']
            user_object = User.objects.get(email=email)
            encrypted_username = computeMD5Hash(user_object.username)

            normal_user_object = models.NormalUser.objects.get(user_id=user_object.id)
            normal_user_object.email_validation_code = encrypted_username
            normal_user_object.save()
            current_site = get_current_site(request)
            html_content = render_to_string('registration/password_reset_email.html',
                                            {
                                                'username': encrypted_username,
                                                'first_name': user_object.first_name,
                                                'last_name': user_object.last_name, 'domain': current_site.domain})
            text_content = strip_tags(html_content)

            connection = mail.get_connection()
            connection.open()
            email1 = mail.EmailMessage(
                'Confirm your account on Social site',
                text_content,
                'sazzad.rupak17@gmail.com',
                [email],
                connection=connection
            )
            email1.send()
            connection.close()
            return render(request, 'registration/password_reset_email_sent.html', {'first_name': user_object.first_name,
                                                                               'last_name': user_object.last_name})
        else:
            return render(request, 'registration/password_reset_form.html', {'reset_form': reset_form})
    else:
        return render(request, 'registration/password_reset_form.html', {'reset_form': reset_form})


def password_recover(request, username):
    if models.NormalUser.objects.filter(email_validation_code=username).count() > 0:
        password_change_form = forms.AccountPasswordChangeForm()
        if request.method == 'POST':
            password_change_form = forms.AccountPasswordChangeForm(request.POST)
            if password_change_form.is_valid():
                new_password = password_change_form.data['password']
                normal_user_object = models.NormalUser.objects.get(email_validation_code=username)
                user_object = models.User.objects.get(id=normal_user_object.user_id)
                user_object.password = make_password(new_password)
                user_object.save()

                normal_user_object.email_validation_code = ''
                normal_user_object.save()

                messages.success(request, "Your password has been updated successfully. Login with new password.")
                return HttpResponseRedirect('/')
        return render(request, 'registration/password_recover_form.html', {'password_change_form': password_change_form})
    else:
        messages.error(request, "No password reset request has been found.")
        return HttpResponseRedirect('/')


@login_required(login_url='login')
def profile(request):
    if request.user.is_authenticated:
        now = datetime.now()
        try:
            profile_data = models.NormalUser.objects.get(user_id=request.user.id)
            page_name = 'Profile'
            user_form = forms.ProfileUpdateForm(instance=models.User.objects.get(id=request.user.id))
            profile_form = forms.UserProfileInfoForm(instance=profile_data)
            image_form = forms.ProfileImageUpload()
            day = profile_data.birth_date.day
            month = profile_data.birth_date.month
            year = profile_data.birth_date.year
            posts_count = Post.objects.filter(user_id=request.user.id).count()
            friends = Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)) &
                                            Q(friendship_status=1)).count()

            # for returning users post

            posts = Post.objects.filter(post_status=True, user_id=request.user.id).order_by('-created_at')

            my_discussion_heads = DiscussionHead.objects.filter(created_by_id=request.user.id)

            return render(request, 'normaluser/profile.html', {'page_name': page_name, 'profile_data': profile_data,
                                                                'user_form': user_form, 'profile_form': profile_form,
                                                                'days': range(1, 32, 1), 'months': range(1, 13, 1),
                                                                'years': range(now.year, 1970, -1), 'birth_day': day,
                                                                'birth_month': month, 'birth_year': year,
                                                                'image_form': image_form, 'posts_count': posts_count,
                                                                'friends_count': friends, 'posts': posts,
                                                                'my_discussion_heads': my_discussion_heads
                                                                })

        except models.NormalUser.DoesNotExist:
            messages.success(request, "You can access your profile view as you have logged in with Social Account.")
            return HttpResponseRedirect('/')


@login_required(login_url='login')
def edit_profile(request):
    if request.user.is_authenticated:
        now = datetime.now()
        profile_data = models.NormalUser.objects.get(user_id=request.user.id)
        page_name = 'Edit Profile'
        user_form = forms.ProfileUpdateForm(instance=models.User.objects.get(id=request.user.id))
        profile_form = forms.UserProfileInfoForm(instance=profile_data)
        image_form = forms.ProfileImageUpload()
        day = profile_data.birth_date.day
        month = profile_data.birth_date.month
        year = profile_data.birth_date.year
        posts_count = Post.objects.filter(user_id=request.user.id).count()
        users_posts = Post.objects.filter(user_id=request.user.id)
        friends = Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)) &
                                        Q(friendship_status=1)).count()

        # for returning users post

        posts = Post.objects.filter(post_status=True, user_id=request.user.id).order_by('-created_at')

        return render(request, 'normaluser/profile-edit.html', {'page_name': page_name, 'profile_data': profile_data,
                                                           'user_form': user_form, 'profile_form': profile_form,
                                                           'days': range(1, 32, 1), 'months': range(1, 13, 1),
                                                           'years': range(now.year, 1970, -1), 'birth_day': day,
                                                           'birth_month': month, 'birth_year': year,
                                                                  'image_form': image_form, 'posts_count': posts_count,
                                                                  'friends_count': friends, 'posts': posts
                                                            })


@login_required(login_url='login')
def update_profile(request):

    if request.method == 'POST':
        user_form = forms.ProfileUpdateForm(request.POST)
        profile_form = forms.UserProfileInfoForm(request.POST)
        if user_form.is_valid():
            user_object = models.User.objects.get(id=request.user.id)
            user_object.first_name = user_form.data['first_name']
            user_object.last_name = user_form.data['last_name']

            user_object.save()

            profile_object = models.NormalUser.objects.get(user_id=request.user.id)

            year = 1970
            if request.POST['year'] != '':
                year = request.POST['year']

            month = 12
            if request.POST['month'] != '':
                month = request.POST['month']

            day = 12
            if request.POST['day'] != '':
                day = request.POST['day']

            profile_object.birth_date = datetime.strptime(str(year) + '-' + str(month) + '-' + str(day),
                                                          "%Y-%m-%d").date()
            profile_object.address = profile_form.data['address']
            profile_object.phone_number = profile_form.data['phone_number']
            profile_object.gender = profile_form.data['gender']

            profile_object.save()
            messages.success(request, "Your profile data has been updated.")
    return redirect('/profile/edit/')


@login_required(login_url='login')
def upload_profile_image(request):
    if request.method == 'POST':
        form = forms.ProfileImageUpload(request.POST, request.FILES)
        if form.is_valid():
            # return HttpResponse(request.FILES['profile_photo'])
            m = models.NormalUser.objects.get(user_id=request.user.id)
            m.profile_photo = request.FILES['profile_photo']
            m.save()
            messages.success(request, "Your profile image has been updated. ")
    # returning base of request url
    next_url = request.POST.get('next_url', '/')  # caller view url for redirecting
    return redirect(next_url)


@login_required(login_url='login')
def user_profile(request, username1):

        profile_username = models.User.objects.get(username=username1)
        profile_data = models.NormalUser.objects.get(user_id=profile_username.id)
        profile_data.username = profile_username.username
        profile_data.first_name = profile_username.first_name
        profile_data.last_name = profile_username.last_name
        profile_data.email = profile_username.email
        page_name = 'Other profile'
        posts = Post.objects.filter(post_status=True, user_id=profile_username.id).order_by('-created_at')
        friend = Friend.objects.filter((Q(user_one_id=request.user.id , user_two_id=profile_username.id) | Q(user_two_id=request.user.id , user_one_id=profile_username.id)) & Q(friendship_status=1)).count()

        friends_count = Friend.objects.filter((Q(user_one_id=profile_username.id ) | Q(user_two_id=profile_username.id )) & Q(friendship_status=1)).count()
        user_discussion_heads = DiscussionHead.objects.filter(created_by_id=profile_username.id)
        return render(request, 'normaluser/user_profile.html', {'page_name': page_name, 'profile_data': profile_data,
                                                                'is_friend': friend, 'posts': posts,
                                                                'posts_count': posts.count(),
                                                                'friends_count': friends_count,
                                                                'user_discussion_heads': user_discussion_heads})


@login_required(login_url='login')
def delete_account(request):
    '''
    Delete a user account
    :param request:
    :return:
    '''
    discussion_recipients = DiscussionRecipient.objects.filter(recipient_id=request.user.id).delete()
    discussion_user_group = DiscussionUserGroup.objects.filter(discussion_user_id=request.user.id).delete()
    discussion = Discussion.objects.filter(sender_id=request.user.id).delete()
    discussion_head = DiscussionHead.objects.filter(created_by_id=request.user.id).delete()
    notification = Notification.objects.filter(to_user_id=request.user.id).delete()
    profile = models.NormalUser.objects.filter(user_id=request.user.id).delete()
    comment = Comment.objects.filter(user_id=request.user.id).delete()
    post = Post.objects.filter(user_id=request.user.id).delete()
    friends = Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id))).delete()
    user = User.objects.get(id=request.user.id).delete()
    return redirect('login')


@login_required(login_url='login')
def user_search(request):
    '''
    Search both user and discussion head for user given value
    :param request:
    :return:
    '''

    # get the user
    users = User.objects.filter(Q(is_superuser=False) & ~Q(id=request.user.id) & (Q(username__iregex=request.GET.get('term')) |
                                                                  Q(first_name__iregex=request.GET.get('term')) |
                                                                  Q(last_name__iregex=request.GET.get('term'))))\
        .distinct('id').values('id', 'first_name', 'last_name', 'username')

    # get the discussion heads
    user_friends = Friend.objects.filter((Q(user_one_id=request.user.id) | Q(user_two_id=request.user.id)) &
                                         Q(friendship_status=1)).all()

    friends_list = [request.user.id]
    for user_friend in user_friends:
        if user_friend.user_one_id == request.user.id:
            friends_list.append(user_friend.user_two_id)
        else:
            friends_list.append(user_friend.user_one_id)
    # return HttpResponse(user_friends)
    heads = DiscussionHead.objects.filter(Q(created_by_id__in=friends_list), Q(head_name__iregex=request.GET.get('term'))).distinct('id').order_by('id',
                                                                                                         'messages__created_at').values('id', 'head_name')
    data = ''
    results = []
    if len(users) > 0:
        for single_user in users:
            user_json = dict()
            user_json['id'] = single_user['id']
            user_json['label'] = single_user['first_name']+' '+single_user['last_name']
            user_json['value'] = single_user['username']
            user_json['url'] = '/profile/other/' + single_user['username']
            results.append(user_json)
        data = JsonResponse(results, safe=False)

    if len(heads) > 0:
        for head in heads:
            head_json = dict()
            head_json['id'] = head['id']
            head_json['label'] = head['head_name']
            head_json['value'] = head['id']
            head_json['url'] = '/discussion/message/' + str(head['id'])
            results.append(head_json)
        data = JsonResponse(results, safe=False)

    return HttpResponse(data)
