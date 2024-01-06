from django.urls import path
from .views import UserRegistrationView, UserLogInView, UserLogOutView, CustomerListView, WorkerListView, \
    WorkerDetailView, CustomerDetailView, UserProfileView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('log-in/', UserLogInView.as_view(), name="log-in"),
    path('log-out/', UserLogOutView.as_view(), name="log-out"),
    path('customers/', CustomerListView.as_view(), name="customers"),
    path('workers/', WorkerListView.as_view(), name="workers"),
    path('worker/<int:pk>', WorkerDetailView.as_view(), name="worker_detail"),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name="customer_detail"),
    path('profile/', UserProfileView.as_view(), name="profile"),
]
