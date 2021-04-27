from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest

from Havwis.core import HavwisWalletUtils, HavwisCryptoWallet
from Havwis import settings

from Wallet.models import NetworkDefinition,  NotificationModel

#home view
class HomeView(View):
  def __init__(self):
    self.template_name = "v_1_0/activity/home/home.html"
  def get(self, request, *args, **kwargs):
    havwis_wallet_utils = HavwisWalletUtils()
    currency_infos = havwis_wallet_utils.getNetworkDefinitionsInfos()
    networks = NetworkDefinition.objects.all()
    notifications = NotificationModel.objects.filter(user=request.user)[:8]
    return render(request, self.template_name, {"currency_infos":currency_infos, "networks":networks, "notifications":notifications})

class WalletView(View):
  def __init__(self):
    self.template_name = "v_1_0/fragments/wallet/wallet.html"
  def get(self, request, *args, **kwargs):
    havwis_wallet_utils = HavwisWalletUtils()
    networks = NetworkDefinition.objects.all()
    currency_infos = havwis_wallet_utils.getNetworkDefinitionsInfos()
    return render(request, self.template_name, {"networks":networks, "currency_infos":currency_infos})
 
class WalletIntentReceiveView(View):
  def __init__(self):
    self.template_name = "v_1_0/fragments/wallet/sub/receive.html"
  def get(self, request, *args, **kwargs):
    network = request.GET.get("network")
    if network is not None:
      address = HavwisCryptoWallet(request).get_address(network=network)
      return render(request, self.template_name, {"network":network, "address":address})
    else:
      return HttpResponseBadRequest()