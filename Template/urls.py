from django.urls import path, include

#imported for views.py [HomeView, ]
from .views import *
import Wallet

urlpatterns = [
  path('home/', HomeView.as_view(), name='home'),
  path('wallet/', WalletView.as_view(), name='wallet'),
  path('wallet/intent/receive/', WalletIntentReceiveView.as_view(), name="receive"),
  path('wallet/intent/', include("Wallet.urls")),
]