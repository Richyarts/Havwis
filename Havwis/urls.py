from django.contrib import admin
from django.urls import path, include

import Authentication

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Authentication.urls'), name="account"),
]
