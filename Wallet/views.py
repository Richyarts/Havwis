#>>>Written by lyonkvalid 7:40PM Wed , jan 6 2020
#>>>Change html template name , @lyonkvalid
from django.views import View
from bitcoinlib.wallets import wallet_exists
from django.core import serializers
from django.http import JsonResponse , HttpResponse
from bitcoinlib.wallets import Wallet
from django.shortcuts import render , get_object_or_404 , redirect
from Wallet.forms import CreditCardForm , VirtualCardForm , SendForm
from Wallet.models import CoinModel , WalletModel , CreditCard
import json
from harvis.core import VirtualCard

#>>>dummy tool to serializer wallet but useless now
class JsonSerializable(object):
  def toJson(self):
    return json.dumps(self.__dict__)
  def __repr__(self):
    return self.toJson()

#>>>The home view
class HomeView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/fragment/HomeFragment.html")
    return redirect("/auth/login/")

#>>>return user wallets and custom_tag check for balance and fiat price using coinmarketapi
class WalletView(View):
  def get(self , request , *args , **kwargs):
    wallet = WalletModel.objects.filter(user = request.user)
    wallet_single = WalletModel.objects.get(user = request.user)
    return render(request , "wallet/fragment/WalletFragment.html" , {"wallet_single":wallet_single , "wallets":wallet})

#>>>Check for wallet_id that user switch to in view and return the wallet object
  def post(self , request , *args , **kwargs):
    wallet_id = request.POST.get("wallet_id")
    if wallet_id != None:
      coins = CoinModel.objects.all()
      wallet = WalletModel.objects.filter(user = request.user)
      wallet_object = Wallet(wallet_id)
      context = {"wallet_object":wallet_object}
      return render(request , "wallet/fragment/WalletFragment.html" , context)
    return JsonResponse(None)

#>>>Payment to fund wallet
class PaymentView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/form/CreditCardActivity.html")
    return redirect("/auth/login/")
  def post(self , request , *args , **kwargs):
    form_data = CreditCardForm(request.POST)
    if form_data.is_valid():
      card_no = form_data.cleaned_data["card_no"]
      card_name = form_data.cleaned_data["card_name"]
      expiry_date = form_data.cleaned_data["expiry_date"]
      cvv = form_data.cleaned_data["cvv"]
      credit_card_object = CreditCard(card_no=card_no , card_name=card_name , expiry_date=expiry_date , cvv=cvv)
      credit_card_object.save()
      return JsonResponse({"status":True})
    return  JsonResponse({"errors":form_data.errors})

#>>>List all user credit cards
class CreditCardView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      wallet_object =  WalletModel.objects.filter(user = request.user)
      return render(request , "wallet/form/CardActivity.html" , {"wallets":wallet_object})
    return redirect("/auth/login/")
 
  def post(self , request , *args , **kwargs):
    pass
 
#>>>VirtualCardView view with stripe virtual card issuing 
class VirtualCardView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/form/RegisterCardActivity.html")
    return redirect("/auth/login/")
  def post(self , request , *args , **kwargs):
    form_data = VirtualCardForm(request.POST)
    profile_object = ProfileModel.objects.get(user = request.user)
    if form_data.is_valid():
      billing_address = form_data.cleaned_data["address"]
      city = form_data.cleaned_data["city"]
      state = form_data.cleaned_data["state"]
      postal_code = form_data.cleaned_data["postal_code"]
      country = form_data.cleaned_data["country"]
      virtual_card = VirtualCard(billing_address , city , state , postal_code , country)
      card_holder = virtual_card.card_holder(profile_object , request.user)
      card = virtual_card.card(card_holder)
      return render(request , "wallet/form/RegisterCardActivity.html" , {"card": card})
    return render(request , "wallet/form/RegisterCardActivity.html" , {"errors": form_data.errors})

#>>>Will work on the send view later >>To do Rest APi for price feed
class SendView(View):
  def get(self , request , *args , **kwargs):
    pass
  def post(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      wallet_id = request.POST["wallet_id"]
      if wallet_exists(wallet_id):
        wallet = Wallet(wallet_id)
        network = request.POST["network"]
        form_data = SendForm(request.POST)
        if form_data.is_valid():
          amount = form_data.cleaned_data["amount"]
          address = form_data.cleaned_data["address"]
          try:
            wallet.send_to(address , amount , network=network)
          except:
            return JsonResponse({"error":"sending error"})
      return render(request , "")
    return redirect("/havwis/login/")

class ReceiveView(View):
  def get(self , request , *args , **kwargs):
    coin_id = kwargs["coin_id"] 
    wallet_id = kwargs["wallet_id"]
    coin = get_object_or_404(CoinModel , id=coin_id)
    network = coin.coin_name
    wallet = Wallet(wallet_id)
    balance = wallet.balance(network=network)
    avatar = coin.coin_avatar
    address = wallet.get_key(network=network).address
    return render(request , "wallet/fragment/ReceiveFragment.html" , {"balance":balance , "coin":coin , "address": address , "network":network , "avatar": avatar})

#>>>Can change to listview but this easy for me @lyonkvalid
class NotificationView(View):
  def get(self ,request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/activity/NotificationsActivity.html")
    return redirect("/havwis/login/")