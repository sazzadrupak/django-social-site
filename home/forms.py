from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Post, Comment


class StatusTextForm(forms.Form):
    status_text = forms.CharField(required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write something to share with your friends',
            'rows': 3,
            'cols': 12,
            'max-length': '200',
        }
    ))

    def clean(self):
        data = self.cleaned_data
        if data.get('status_text') == '':
            raise forms.ValidationError('Please write something before post.')
        data['status_text'] = data.get('status_text')

        return data

    class Meta:
        model = Post
        fields = ['status_text']


def must_be_empty(value):
    if value:
        raise forms.ValidationError('is not empty')


class CommentTextForm(forms.Form):
    comment_text = forms.CharField(required=True, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Add comment here',
            'max-length': '100',
        }
    ))
    honeypot = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave empty", validators=[must_be_empty])

    def clean(self):
        data = self.cleaned_data
        if data.get('comment_text') == '':
            raise forms.ValidationError('Please write something before post.')
        data['comment_text'] = data.get('comment_text')

        return data

    class Meta:
        model = Comment
        fields = ['comment_text']
