from django import forms
from .models import NormalUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your e-mail address here'
        }
    ),
        required=True
    )

    password = forms.CharField(label="Password", widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your password here'
        }
    ),
        required=True
    )

    def clean(self):
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        try:
            user_object = User.objects.get(email=email)
        except User.DoesNotExist:
            user_object = None

        if user_object is not None:
            if user_object.is_active is False:
                raise forms.ValidationError("Your account has not been active yet. Check your email inbox for "
                                            "activation link.")
            else:
                user = authenticate(username=user_object.username, password=password)
                if user is None:
                    raise forms.ValidationError('Please check your email address and password again.')
        else:
            raise forms.ValidationError('The email you have entered, does not match any account.')

        data['email'] = email
        data['password'] = password
        return data


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your password here',
            'required': 'true',
            'min_length': 8
        },
    ),
        required=True,
        help_text='Password must be 8 characters minimum length (with at least 1 lower case, 1 upper case and 1 number)'
                  '.'
    )

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your password again here',
        }
    ),
        required=True,
        help_text='Re-write your password again'
    )

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your first name here'
        }
    ),
        required=True,
    )

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your last name here'
        }
    ),
        required=True,
    )

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your user name here'
        }
    ),
        required=True,
    )

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your email address here'
        }
    ),
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name", "username", "email", "password")

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        email = data.get("email")
        username = data.get("username")

        # check password and confirm password match
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm password does not match"
            )

        # check password length
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')

        # check for digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least 1 digit.')

        # check for uppercase
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Password must contain at least 1 uppercase letter')

        # check for lowercase
        if not any(char.islower() for char in password):
            raise forms.ValidationError('Password must contain at least 1 lowercase letter')

        # check email validation
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This E-mail address already used. Try with new one."
            )

        # check username validation
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError(
                "This User name already used. Try with new one."
            )
        data['first_name'] = data.get('first_name')
        data['last_name'] = data.get('last_name')
        data['username'] = username
        data['email'] = email
        data['password'] = password
        return data


class UserProfileInfoForm(forms.ModelForm):

    address = forms.CharField(required=False, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your address here'
        }
    ))

    phone_number = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your phone number here'
        }
    ))

    GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female')
    )

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect(
    ))

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserProfileInfoForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['address'].required = False
        self.fields['phone_number'].required = False
        # self.fields['birth_date'].required = False

    def clean(self):
        data = self.cleaned_data
        phone_number = data.get("phone_number")
        gender = data.get("gender")
        address = data.get("address")

        data['address'] = address
        data['phone_number'] = phone_number
        data['gender'] = gender
        return data

    class Meta:
        model = NormalUser
        fields = ["address", "phone_number", "gender"]


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your email address here'
        }
    ))

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['email'].required = True

    def clean(self):
        data = self.cleaned_data
        email = data.get("email")

        # check email validation
        if User.objects.filter(email=email).count() > 0:
            pass
        else:
            raise forms.ValidationError(
                "No account has been found against your email address."
            )
        data['email'] = email
        return data


class AccountPasswordChangeForm(forms.Form):
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your new password here'
        }
    ))

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(AccountPasswordChangeForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['password'].required = True

    def clean(self):
        data = self.cleaned_data
        password = data.get("password")
        username = data.get("username")

        # check password length
        if len(password) < 8:
            raise forms.ValidationError('Password must be at least 8 characters long.')

        # check for digit
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Password must contain at least 1 digit.')

        # check for uppercase
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Password must contain at least 1 uppercase letter')

        # check for lowercase
        if not any(char.islower() for char in password):
            raise forms.ValidationError('Password must contain at least 1 lowercase letter')

        data['password'] = password
        return data


class ProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your first name here'
        }
    ),
        required=True,
    )

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Write your last name here'
        }
    ),
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "first_name", "last_name")

    def clean(self):
        data = self.cleaned_data

        data['first_name'] = data.get('first_name')
        data['last_name'] = data.get('last_name')
        return data


class ProfileImageUpload(forms.ModelForm):
    profile_photo = forms.ImageField(label="Profile photo", required=True, widget=forms.FileInput(attrs= {'class':'form-control'}))

    class Meta:
        model = NormalUser
        fields = ("profile_photo", )
