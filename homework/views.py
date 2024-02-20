from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from account.models import UserAccount


# custom 404 view
def custom_404(request, exception):
    return render(request, 'homework/404.html', status=404)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email:
            if request.user.role == 'worker':
                return redirect("user/account/customers/")
            else:
                return redirect("user/account/workers/")
        else:
            if "_auth_user_id" in request.GET:
                login(request, UserAccount.objects.get(pk=request.GET.get("_auth_user_id")))
                return redirect("/")
            return render(request, 'homework/home.html')
