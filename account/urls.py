from django.urls import path
from .views import UserRegistrationView, UserLogInView, UserLogOutView


urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('log-in/', UserLogInView.as_view(), name="log-in"),
    path('log-out/', UserLogOutView.as_view(), name="log-out"),
]
