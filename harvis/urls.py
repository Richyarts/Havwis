from django.contrib import admin
from django.conf import settings
from django.urls import path , include , re_path
from django.conf.urls.static import static
from Wallet import views
import Authentication
import Wallet
import notifications.urls
import Api

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('auth/',include('Authentication.urls') , name="auth"),
    path('havwis/' , include('Wallet.urls') , name="havwis"),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path("debug/" , views.debug , name="debug"),
    path("api/" , include("Api.urls") , name="api"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

