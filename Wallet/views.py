from django.views import View
from django.shortcuts import render
from Wallet.models import CoinModel

class HomeView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/home.htm")

class WalletView(View):
  def get(self , request , *args , **kwargs):
    coins = CoinModel.objects.all()
    return render(request , "wallet/wallet.htm" , {"coins":coins})