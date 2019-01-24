from django import forms
from django.contrib.auth.models import User
from .models import Discussion, DiscussionHead, DiscussionRecipient, DiscussionUserGroup


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class DiscussionHeadForm(forms.Form):
    head_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Add new discussion head',
            'max-length': '255',
        }
    ))

    def clean(self):
        data = self.cleaned_data
        if data.get('head_name') == '':
            raise forms.ValidationError('Please write something before post.')

        if DiscussionHead.objects.filter(head_name=data.get('head_name')).exists():
            raise forms.ValidationError(
                "This head name already used. Try with new one."
            )
        data['head_name'] = data.get('head_name')

        return data

    class Meta:
        model = DiscussionHead
        fields = ['head_name']


class DiscussionForm(forms.Form):
    message = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'write_msg',
            'max-length': '255',
            'placeholder': 'Type a message'
        }
    ))

    discussion_head_id = forms.CharField(required=True, widget=forms.HiddenInput)

    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty",
                               validators=[must_be_empty])

    def clean(self):
        data = self.cleaned_data
        data['message'] = data.get('message')
        data['discussion_head_id'] = data.get('discussion_head_id')
        return data

    class Meta:
        model = Discussion
        fields = ['message', 'discussion_head_id']
