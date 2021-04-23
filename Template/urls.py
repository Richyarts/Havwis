from django.urls import path

#imported for views.py [HomeView, ]
from .views import *

urlpatterns = [
  path('home/', HomeView.as_view(), name='home'),
  path('wallet/', WalletView.as_view(), name='wallet'),
  path('wallet/intent/receive/', WalletIntentReceiveView().as_view(), name="receive"),
]