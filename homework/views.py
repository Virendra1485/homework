from django.shortcuts import render, redirect
from django.views import View


# custom 404 view
def custom_404(request, exception):
    return render(request, 'homework/404.html', status=404)


class HomeView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.email:
            return redirect("user/account/customers/")
        else:
            return render(request, 'homework/home.html')
