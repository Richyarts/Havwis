from django.urls import path
from Wallet.views import BuyView , VirtualCardView , SendView , ReceiveView ,  HomeView , WalletView , CreditCardView , NotificationView , PaymentView

urlpatterns = [
  path("home/" , HomeView.as_view() , name="home"),
  path("wallet/" , WalletView.as_view() , name="wallet"),
  path("pay/" , PaymentView.as_view() , name="creditcard"),
  path("card/" , CreditCardView.as_view() , name="cards"),
  path("virtualcard/" , VirtualCardView.as_view() , name="virtualcard"),
  path("notifications/<int:id>/" , NotificationView.as_view() , name="notifications"),
  path("receive/<int:coin_id>/<wallet_id>/" , ReceiveView.as_view() , name="receive"),
  path("send/<int:coin_id>/<wallet_id>/"  , SendView.as_view() , name="send"),
  path("buy/<int:network_id>/" , BuyView.as_view() , name="buy"),
]