from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Friend
from django.db.models import Q


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class FriendRequestSendForm(forms.Form):
    user_one_id = forms.IntegerField(required=True, widget=forms.HiddenInput,)
    user_two_id = forms.IntegerField(required=True, widget=forms.HiddenInput,)
    lead_user_id = forms.IntegerField(required=True, widget=forms.HiddenInput, )

    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty",
                               validators=[must_be_empty])

    def clean(self):
        data = self.cleaned_data
        user_one_id = data.get('user_one_id')
        user_two_id = data.get('user_two_id')
        if Friend.objects.filter((Q(user_one_id=user_one_id) & Q(user_two_id=user_two_id))).count() > 0 \
                or Friend.objects.filter((Q(user_one_id=user_two_id) & Q(user_two_id=user_one_id))).count() > 0:
            raise forms.ValidationError(
                "Two users are already connected."
            )
        else:
            pass

        data['user_one_id'] = user_one_id
        data['user_two_id'] = user_two_id

        return data
