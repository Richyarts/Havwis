from django.shortcuts import render, redirect
from django.views import View
from django.https import HttpResponseBadRequest

from Havwis.core import HavwisWalletUtils, HavwisCryptoWallet
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
    havwis_wallet_utils = HavwisWalletUtils()
    if not settings.DEBUG:
      networks = [{"network":"testnet", "symbol":"TBTC"}, {"network":"litecoin_testnet", "symbol":"TLTC"}]
      return render(request, self.template_name, {"networks":networks})
    else:
      networks = NetworkDefinition.objects.all()
      currency_infos = havwis_wallet_utils.getNetworkDefinitionsInfos()
      return render(request, self.template_name, {"networks":networks, "currency_infos":currency_infos})
 
class WalletIntentReceiveView(View):
  def __init__(self):
    self.template_name = "v_1_0/fragments/sub/receive.html"
  def get(self, request, *args, **kwargs):
    network = request.GET.get()
    if networks is not None:
      address = HavwisCryptoWallet().get_address(network=network)
      return render(request, self.template_name, {"network":network, "address":address})
    else:
      return HttpResponseBadRequest()