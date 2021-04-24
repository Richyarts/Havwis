from django.contrib import admin
from django.urls import path, include

import Authentication
import Template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qr_code/', include('qr_code.urls', namespace="qr_code")),
    path('account/', include('Authentication.urls'), name="account"),
    path('activity/', include('Template.urls'), name='activity'),
]
