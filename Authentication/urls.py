from django.urls import path, include
import django.contrib.auth.urls 

urlpatterns = [
  path("", include("django.contrib.auth.urls")),
]