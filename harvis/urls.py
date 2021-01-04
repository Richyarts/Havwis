from django.contrib import admin
from django.conf import settings
from django.urls import path , include
from django.conf.urls.static import static
import Authentication
import Wallet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('Authentication.urls') , name="auth"),
    path('harvis/' , include('Wallet.urls') , name="harvis"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

