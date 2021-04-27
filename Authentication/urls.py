from django.urls import path, include
import django.contrib.auth.urls 

from .views import SignUpView, updateData

urlpatterns = [
  path("", include("django.contrib.auth.urls")),
  path("register/", SignUpView.as_view(), name="register"),
  path("update/<type>/", updateData, name="update"),
]