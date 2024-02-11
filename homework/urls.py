from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import custom_404, HomeView


handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/account/', include("account.urls")),
    path('', HomeView.as_view(), name="home"),
    path('chats/', include("chat.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

