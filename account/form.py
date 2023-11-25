from django import forms
from .models import UserAccount
from django.contrib.auth.forms import AuthenticationForm


class UserSignUpForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = (
            "first_name",
            "last_name",
            "email",
            "password",
            "working_days",
            "amount",
            "description",
            "profile_picture"
        )