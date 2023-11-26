from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/account/', include("account.urls")),
    path('', TemplateView.as_view(template_name="homework/home.html"), name="home"),
]
