from django.shortcuts import redirect, render
from django.views import View
from django.http import Http404, HttpResponseBadRequest, JsonResponse, HttpResponse

from .forms import SendForm
from .models import SendModel

from bitcoinlib.wallets import Wallet
from bitcoinlib.networks import NETWORK_DEFINITIONS

from Havwis.utils import Binance
from Havwis.core import HavwisTransaction

from Wallet.models import NotificationModel

#Dummy send view to upgrade later @lyonkvalid
class SendView(View):
  def __init__(self):
    self.template_name = "v_1_0/fragments/wallet/sub/send.html"
  
  def get(self, request, *args, **kwargs):
    network = request.GET.get("network")
    try:
      binance = Binance()
    except:
      binance = None
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
              json_fee_result = havwis_transaction.get_transaction_fee(request)
              return JsonResponse(json_fee_result)
            except Exception as e:
              return JsonResponse({"status":False, "data":{"error": str(e)}})
          else:
            return JsonResponse({"status":False, "data":{"error":"Low balance, fund wallet to continue transaction"}})
        if next == "save":
          havwis_transaction = HavwisTransaction(wallet=wallet, amount=amount, network=network, address=address)
          #todo encapsulate this in a function
          tx_fee = float(request.POST["fee"])
          havwis_percentage = tx_fee - 450
          response = havwis_transaction.send(address, fee=300)
          havwis_reponse = havwis_transaction.send(address, fee=150)
          if response["status"] and havwis_reponse["status"]:
            send_model_object = SendModel(sender=request.user, address=address, amount=amount, network=next)
            send_model_object.save()
            currency_code = NETWORK_DEFINITIONS[network]["currency_code"]
            notification = NotificationModel(user=user, type="send", header="{}Sent".format(currency_code), text="Sent {} to {}.".format(str(amount)+" "+currency_code, address), number=amount)
            notification.save()
            return JsonResponse({"status":True, "data":{"msg":{"next":"success"}}})
          else:
            return JsonResponse({"status":False, "data_1":response, "data_2":havwis_reponse})
        elif next == "pin":
          pin = request.POST.get("pin")
          if int(pin) == user.transaction_pin:
            return JsonResponse({"status":True, "data":{"msg":{"next":"success"}}})
          elif pin is None:
            return JsonResponse({"status":False, "data":{"error":"Pin is not provided"}})
          else:
            print(pin, user.transaction_pin)
            return JsonResponse({"status":False, "data":{"error":"Invalid pin"}})
      else:
        return HttpResponseBadRequest()
    else:
      return JsonResponse({"status":False,"type":"form", "data":{"error":form_data.errors}})