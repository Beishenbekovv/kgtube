from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "channel_name",
            "photo"
        ]


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username", "password",
            "first_name", "last_name"
        ]

class UserAuthForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        fields = ["username", "password"]
   