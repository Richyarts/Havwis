from django.shortcuts import render, redirect
from django.views import View

from Havwis.utils import binance

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
    networks = NetworkDefinition.objects.all()
    prices = binance.get_price()
    return render(request, self.template_name, {"networks":networks, "prices":prices})