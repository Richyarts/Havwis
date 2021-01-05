from django.urls import path
from Wallet.views import HomeView , WalletView , CreditCardView

urlpatterns = [
  path("home/" , HomeView.as_view() , name="home"),
  path("wallet/" , WalletView.as_view() , name="wallet"),
  path("creditcard/" , CreditCardView.as_view() , name="creditcard"),
]