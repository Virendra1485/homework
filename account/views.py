import os

import qrcode
from io import BytesIO
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.views.generic import CreateView, View, DetailView, ListView, DeleteView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .form import UserSignUpForm, UpdateProfilePictureForm, UpdatePersonalInfoForm, UpdateUserPreferenceForm
from .models import UserAccount
from stripe_utils import StripeHelpers


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
        if role == 'customer':
            stripe_customer_id = StripeHelpers().create_customer(form.cleaned_data['email'])
            self.object.stripe_customer_id = stripe_customer_id
        self.object.save()
        return response


class UserLogInView(LoginView):
    template_name = "account/login.html"

    def get_success_url(self):
        user = self.request.user
        self.create_qr_image()
        if user is None:
            return reverse_lazy("log-in")
        elif user.role == "customer":
            return reverse_lazy('workers') + '?page=1'
        elif user.role == "worker":
            return reverse_lazy('customers') + '?page=1'
        else:
            return reverse_lazy('home')

    def create_qr_image(self):
        # Generate QR code
        user = self.request.user
        data = f"https://{os.environ.get('HOST')}?_auth_user_id={self.request.session._session_cache['_auth_user_id']}&_auth_user_hash={self.request.session._session_cache['_auth_user_hash']}&_auth_user_backend={self.request.session._session_cache['_auth_user_backend']}&_SessionBase__session_key={self.request.session._SessionBase__session_key}".replace('"', '')
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4,)
        qr.add_data(data)
        qr.make(fit=True)

        # Create an image from the QR Code instance
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save the image to a BytesIO buffer
        buffer = BytesIO()
        qr_image.save(buffer, format="PNG")
        image_file = ContentFile(buffer.getvalue())
        if user.qr_picture:
            default_storage.delete(user.qr_picture.path)

        file_path = default_storage.save('qr_pictures/generated.png', image_file)
        user.qr_picture = file_path
        user.save()
        return "response"


class UserLogOutView(View):
    def get(self, request):
        self.request.user.qr_picture.delete()
        logout(request)
        return redirect("log-in")


class CustomerListView(LoginRequiredMixin, ListView):
    model = UserAccount
    template_name = "account/customers.html"
    context_object_name = "customers"
    paginate_by = 5

    def get_queryset(self):
        return UserAccount.objects.filter(role="customer")


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['update_profile_picture_form'] = UpdateProfilePictureForm()
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = UserAccount
    success_url = reverse_lazy('home')
    template_name = 'account/user_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            return redirect('home')
        obj.profile_picture.delete()
        obj.qr_picture.delete()
        return obj


class UpdateProfilePictureView(UpdateView):
    model = UserAccount
    form_class = UpdateProfilePictureForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        self.request.user.profile_picture.delete()
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdatePersonalInfo(LoginRequiredMixin, UpdateView):
    model = UserAccount
    template_name = "account/update_personal_info.html"
    form_class = UpdatePersonalInfoForm
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        # self.request.user.profile_picture.delete()
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super().form_valid(form)


class UpdateUserPreferenceView(LoginRequiredMixin, UpdateView):
    model = UserAccount
    template_name = "account/preference.html"
    form_class = UpdateUserPreferenceForm
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = self.request.user
        return super().form_valid(form)


class QrView(LoginRequiredMixin, TemplateView):
    model = UserAccount
    template_name = "account/my_qr.html"
