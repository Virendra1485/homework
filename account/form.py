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
            "blocker",
        )


class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['profile_picture']


class UpdatePersonalInfoForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['first_name', 'description']


class UpdateUserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserAccount
        fields = ['location_city', 'location_country', 'location_address', 'working_days', 'blocker']