from django.urls import path
from django.contrib.auth.views import TemplateView
from .views import UserRegistrationView, UserLogInView, UserLogOutView, CustomerListView, WorkerListView, \
    WorkerDetailView, CustomerDetailView, UserProfileView, UserDeleteView

urlpatterns = [
    path('registration/', UserRegistrationView.as_view(), name="registration"),
    path('log-in/', UserLogInView.as_view(), name="log-in"),
    path('log-out/', UserLogOutView.as_view(), name="log-out"),
    path('customers/', CustomerListView.as_view(), name="customers"),
    path('workers/', WorkerListView.as_view(), name="workers"),
    path('worker/<int:pk>', WorkerDetailView.as_view(), name="worker_detail"),
    path('customer/<int:pk>', CustomerDetailView.as_view(), name="customer_detail"),
    path('profile/', UserProfileView.as_view(), name="profile"),
    # path('confirm-delete', TemplateView.as_view(template_name="account/user_confirm_delete.html"), name="confirm-delete"),
    path('delete/<int:pk>', UserDeleteView.as_view(), name="delete-user"),
]
