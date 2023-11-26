from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .form import UserSignUpForm
from django.contrib.auth import login, logout


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
        login(self.request, self.object)
        return response


class UserLogInView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        user = self.request.user
        if user is None:
            return reverse_lazy("signin")
        elif user.role == "customer":
            return reverse_lazy('workers') + '?page=1'
        elif user.role == "worker":
            return reverse_lazy('customers') + '?page=1'
        else:
            return reverse_lazy('home')


class UserLogOutView(View):
    def get(self, request):
        logout(request)
        return redirect("signin")
