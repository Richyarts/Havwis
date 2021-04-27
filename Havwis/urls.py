from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import Authentication
import Template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('account/', include('Authentication.urls'), name="account"),
    path('activity/', include('Template.urls'), name='activity'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
