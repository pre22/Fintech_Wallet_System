import random
import string
from django import forms
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm
)

from .models import (
    CustomUser,
    NewsLetter
)


class CustomUserCreationForm(UserCreationForm):
    '''Custom UserCreationForm'''
    class Meta:
        '''Meta'''
        model = CustomUser
        fields = UserCreationForm.Meta.fields


class CustomUserChangeForm(UserChangeForm):
    '''Custom UserChangeForm'''
    class Meta:
        '''Meta'''
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "gender",
            "username",
            "password",
        )


class SignupForm(UserCreationForm):
    '''Signup Form'''

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your First Name",
                "name": "first_name",
                "id": "firt_name",
            }
        )

        self.fields["last_name"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your Last Name",
                "name": "last_name",
                "id": "last_name",
            }
        )

        self.fields["email"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your email address",
                "name": "email",
                "id": "email",
            }
        )

        self.fields["country"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Choose your country of residence",
                "name": "country",
                "id": "country",
            }
        )

        self.fields["gender"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Choose your gender",
                "name": "gender",
                "id": "gender",
            }
        )

        self.fields["logo"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Upload Your Profile Pics",
                "name": "logo",
                "id": "logo",
            }
        )

        self.fields["referral_code"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Referral Code (if any)",
                "name": "referral_code",
                "id": "referral_code",
            }
        )

        self.fields["phone"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter a Valid Phone Number with country code",
                "name": "phone",
                "id": "phone",
            }
        )

        self.fields["referral_code"].required = False

        self.fields["password1"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your Password",
                "name": "password",
                "id": "password",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Confirm your Password",
                "name": "password2",
                "id": "password",
            }
        )

    class Meta(UserCreationForm.Meta):
        '''Meta'''

        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "country",
            "gender",
            "logo",
            "referral_code",
            "phone",
            "password1",
            "password2",
        )

    def save(self, request):
        user = super(SignupForm, self).save(request)

        user.is_active = True
        user.referral_code = "{}-{}".format(self.cleaned_data['first_name'], ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=8)))
        # Password Validation
        password1 = self.cleaned_data["password1"]
        password2 = self.cleaned_data["password2"]

        if password2 != password1:
            raise forms.ValidationError("Passwords don't match")

        user.set_password(password2)

        user.save()
        return user


class NewsletterForm(forms.ModelForm):
    '''Harvests user email for newsletter subscription'''

    def __init__(self, *args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)

        self.fields["subscriber"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Enter your Email Address",
                "name": "subscriber",
                "id": "subscriber",
            }
        )

    class Meta:
        model = NewsLetter
        fields = ("subscriber",)
