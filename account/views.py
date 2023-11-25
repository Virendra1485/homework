from django.views.generic import CreateView
from .form import UserSignUpForm
from django.contrib.auth import login


class UserRegistrationView(CreateView):
    form_class = UserSignUpForm
    success_url = "/user/account/log-in/"
    template_name = "account/registration.html"

    def form_valid(self, form):
        form.instance.role = "worker"
        response = super().form_valid(form)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        login(self.request, self.object)
        return response
