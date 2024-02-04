import os
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View, DetailView, ListView, DeleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .form import UserSignUpForm
from .models import UserAccount


class UserRegistrationView(CreateView):
    form_class = UserSignUpForm
    success_url = "/user/account/log-in/"
    template_name = "account/registration.html"

    def form_valid(self, form):
        role = self.request.GET.get("role")
        if not role:
            return redirect("home")
        form.instance.role = role
        response = super().form_valid(form)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        return response


class UserLogInView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        user = self.request.user
        if user is None:
            return reverse_lazy("log-in")
        elif user.role == "customer":
            return reverse_lazy('workers') + '?page=1'
        elif user.role == "worker":
            return reverse_lazy('customers') + '?page=1'
        else:
            return reverse_lazy('home')


class UserLogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("log-in")


class CustomerListView(LoginRequiredMixin, ListView):
    model = UserAccount
    template_name = "account/customers.html"
    context_object_name = "customers"
    paginate_by = 5

    def get_queryset(self):
        return UserAccount.objects.filter(role="customer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WorkerListView(LoginRequiredMixin, ListView):
    model = UserAccount
    template_name = "account/workers.html"
    context_object_name = "workers"
    paginate_by = 5

    def get_queryset(self):
        return UserAccount.objects.filter(role="worker")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class WorkerDetailView(DetailView):
    model = UserAccount
    template_name = 'account/worker_detail.html'
    context_object_name = 'worker'


class CustomerDetailView(DetailView):
    model = UserAccount
    template_name = 'account/customer_detail.html'
    context_object_name = 'customer'


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserAccount
    template_name = 'account/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.id)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = UserAccount
    success_url = reverse_lazy('home')
    template_name = 'account/user_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            return redirect('home')
        return obj

    # def delete(self, request, *args, **kwargs):
    #     user = self.get_object()
    #     if user.profile_picture:
    #         file_path = user.profile_picture.path
    #         breakpoint()
    #         if os.path.exists(file_path):
    #             os.remove(file_path)
    #     user.delete()
    #     return redirect(self.success_url)
