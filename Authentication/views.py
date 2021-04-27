from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import authenticate
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model

from Havwis.core import HavwisCryptoWallet

from .models import User
from .forms import SignUpForm

class SignUpView(View):
  template_name = "registration/signup.html"
  def get(self, request, *args, **kwargs):
    return render(request, self.template_name)
  def post(self, request, *args, **kwargs):
    form_data = SignUpForm(request.POST)
    havwis_crypto_wallet = HavwisCryptoWallet(request)
    if form_data.is_valid():
      email = form_data.cleaned_data["email"]
      password = form_data.cleaned_data["password1"]
      first_name = form_data.cleaned_data["first_name"]
      last_name = form_data.cleaned_data["last_name"]
      phone_number = form_data.cleaned_data["phone_number"]
      try:
        wallet_id = havwis_crypto_wallet.create_wallet(get_random_string())
        user = User(email=email, password=password, phone_number=phone_number, first_name=first_name, last_name=last_name)
        user.wallet_id = wallet_id
        user.save()
      except Exception as e:
        return JsonResponse({"status":False, "errors":{"error":e.args[0]}})
      user = authenticate(request, username=email, password=password)
      print(user)
      if user is not None:
        return JsonResponse({"status":True, "user": True})
      else:
        return JsonResponse({"status":True, "user":None})
    else:
      return JsonResponse({"status":False, "errors":form_data.errors})

def updateData(request, *args, **kwargs):
  user = request.user
  if request.method == 'POST':
    if kwargs["type"] == "tx_pin":
      pin = request.POST.get("pin")
      next = request.POST.get("next")
      if pin is not None:
        user.transaction_pin = pin 
        user.save()
        return JsonResponse({"status":True, "data":{"next":next}})
      return JsonResponse({"status":False, "data":{"errors":"You don't provide a pin"}})