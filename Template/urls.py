from django.urls import path

#imported for views.py [HomeView, ]
from .views import *

urlpatterns = [
  path('home/', HomeView.as_view(), name='home'),
]