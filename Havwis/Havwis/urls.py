from django.contrib import admin
from django.urls import path, include

import Authentication
import Template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Authentication.urls'), name="account"),
    path('activity/', include('Template.urls'), name='activity'),
]
