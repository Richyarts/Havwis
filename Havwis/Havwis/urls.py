from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

import Authentication
import Template

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Authentication.urls'), name="account"),
    path('activity/', include('Template.urls'), name='activity'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
