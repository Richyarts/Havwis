from django.shortcuts import redirect, render
from django.views import View
from django.http import Http404, HttpResponseBadRequest, JsonResponse

from .forms import SendForm
from .models import SendModel

from bitcoinlib.wallets import Wallet
from bitcoinlib.networks import NETWORK_DEFINITIONS

from Havwis.utils import binance
from Havwis.core import HavwisTransaction

#Dummy send view to upgrade later @lyonkvalid
class SendView(View):
  def __init__(self):
    self.template_name = "v_1_0/fragments/wallet/sub/send.html"
  
  def get(self, request, *args, **kwargs):
    network = request.GET.get("network")
    if network is not None:
      if binance is not None:
        info = list(filter(lambda info: info["symbol"] == NETWORK_DEFINITIONS[network]["currency_code"], binance.pure_price()))
        balance = Wallet(request.user.wallet_id).balance(network=network)
        return render(request, self.template_name, {"network":network, "info":info, "balance":balance})
      else:
        return HttpResponse("<h4> Connect to Internet </h4>")
    else:
      return HttpResponseBadRequest()

  #dummy send getaway to upgrade later @lyonkvalid
  def post(self, request, *args, **kwargs):
    form_data = SendForm(request.POST)
    user = request.user
    wallet = Wallet(request.user.wallet_id)
    next = request.GET.get("next")
    if form_data.is_valid():
      #could just have unpack the dict pls help me do it @lyonkvalid
      network = form_data.cleaned_data["network"]
      address = form_data.cleaned_data["address"]
      amount= form_data.cleaned_data["amount"]
      if next is not None:
        if next == "fee":
          amount = request.POST.get("amount")
          if float(amount) > 0:
            try:
              havwis_transaction = HavwisTransaction(wallet=wallet, amount=amount, network=network, address=address)
              return JsonResponse(havwis_transaction.get_transaction_fee(request))
            except Exception as e:
              return JsonResponse({"status":False, "data":{"error": str(e)}})
          else:
            return JsonResponse({"status":False, "data":{"error":"Low balance, fund wallet to continue transaction"}})
        if next == "save":
          send_model_object = SendModel(user=request.user, address=address, amount=amount, network=next)
          send_model_object.save(commit=False)
          return JsonResponse({"status":True, "data":{"msg":{"next":"pin"}}})
        elif next == "pin":
          pin = request.POST.get("pin")
          if pin == user.transaction_pin:
            return JsonResponse({"status":True, "data":{"msg":{"next":"success"}}})
          else:
            return JsonResponse({"status":False, "data":{"error":"Invalid pin"}})
      else:
        return HttpResponseBadRequest()
    else:
      return JsonResponse({"status":False, "data":{"error":form_data.errors}})