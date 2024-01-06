from django import forms
from .models import UserAccount


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
            "profile_picture",
            "location_country",
            "location_city",
        )
