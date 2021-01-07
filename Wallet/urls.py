from django.urls import path
from Wallet.views import VirtualCardView , ReceiveView ,  HomeView , WalletView , CreditCardView , NotificationView , PaymentView

urlpatterns = [
  path("home/" , HomeView.as_view() , name="home"),
  path("wallet/" , WalletView.as_view() , name="wallet"),
  path("pay/" , PaymentView.as_view() , name="creditcard"),
  path("card/" , CreditCardView.as_view() , name="cards"),
  path("virtualcard/" , VirtualCardView.as_view() , name="virtualcard"),
  path("notifications/<int:id>/" , NotificationView.as_view() , name="notifications"),
  path("receive/<int:coin_id>/<wallet_id>/" , ReceiveView.as_view() , name="receive"),
]