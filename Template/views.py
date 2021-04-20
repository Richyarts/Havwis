from django.shortcuts import render, redirect
from django.views import View

from Havwis.utils import binance
from Havwis import settings

from Wallet.models import NetworkDefinition

#home view
class HomeView(View):
  def __init__(self):
    self.template_name = "v_1_0/activity/home/home.html"
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)

class WalletView(View):
  def __init__(self):
    self.template_name = "v_1_0/fragments/wallet/wallet.html"
  def get(self, request, *args, **kwargs):
    if settings.DEBUG:
      networks = [{"network":"testnet", "symbol":"TBTC"}, {"network":"litecoin_testnet", "symbol":"TLTC"}]
      return render(request, self.template_name, {"networks":networks})
    else:
      networks = NetworkDefinition.objects.all()
      prices = binance.get_price()
      return render(request, self.template_name, {"networks":networks, "prices":prices})