#>>>Written by lyonkvalid 7:40PM Wed , jan 6 2020
#>>>Change html template name , @lyonkvalid
from django.views import View
from Authentication.models import CustomerModel , ProfileModel
from bitcoinlib.wallets import wallet_exists
from django.core import serializers
from django.http import JsonResponse , HttpResponse
from bitcoinlib.wallets import Wallet
from django.shortcuts import render , get_object_or_404 , redirect
from Wallet.forms import CreditCardForm , VirtualCardForm , SendForm , TextForm , IntegerForm
from Wallet.models import CoinModel , TradeModel , WalletModel , CreditCard , VirtualCardModel
import json
from harvis import paystack
from Api import flutterwave
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
      if not WalletModel.objects.get(user = request.user).credit_card.filter(label="crytocurrency").exists:
        return render(request , "wallet/fragment/HomeFragment.html" , {"trade_coins":TradeModel.objects.all()})
      return render(request , "wallet/fragment/HomeFragment.html" , {"trade_coins":TradeModel.objects.all() , "create":"create"})
    return redirect("/auth/login/")
  def post(self , request , *args , **kwargs):
    pass
  
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
      card =  WalletModel.objects.get(user = request.user).credit_card.all()
      return render(request , "wallet/form/CardActivity.html" , {"card": card})
    return redirect("/auth/login/")
 
  def post(self , request , *args , **kwargs):
    amount = request.POST["amount"]
    card_id = request.POST["id"]
    type = request.POST["type"]
    if type == "exist":
      if flutterwave.GetBalance(card_id) != 0 and amount < flutterwave.GetBalance(card_id):
        profile = ProfileModel.objects.get(user = request.user)
        id = flutterwave.CreateCard(request.user , profile , amount , currency)
        card = CreditCard(id)
        wallet = WalletModel.objects.get(user = request.user).credit_card.add(card)
        return JsonResponse({"status":"Card created"})
      return JsonResponse({"can't create card"})
    elif type == "paystack":
      pass
      
#>>>VirtualCardView view with stripe virtual card issuing 
class VirtualCardView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      if VirtualCardModel.objects.filter(user = request.user).exists:
        return render(request , "wallet/form/RegisterCardActivity.html")
      return JsonResponse({"status":"True"})
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
      return redirect("/havwis/card/")
    return render(request , "wallet/form/RegisterCardActivity.html" , {"errors": form_data.errors})

#>>>Will work on the send view later >>To do Rest APi for price feed
class SendView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
     coin_id = kwargs["coin_id"] 
     wallet_id = kwargs["wallet_id"]
     coin = get_object_or_404(CoinModel , id=coin_id)
     network = coin.coin_name
     wallet = Wallet(wallet_id)
     balance = wallet.balance(network=network)
     avatar = coin.coin_avatar
     return render(request , "wallet/fragment/SendFragment.html" , {"id":wallet_id , "balance":balance , "coin":coin , "network":network , "avatar": avatar})
    else:
      return redirect("/auth/login/")
      
  def post(self , request , *args , **kwargs):
    wallet_id = kwargs["wallet_id"]
    coin_id = kwargs["coin_id"] 
    coin = get_object_or_404(CoinModel , id=coin_id)
    network = coin.coin_name
    if request.user.is_authenticated:
      if wallet_exists(wallet_id):
        wallet = Wallet(wallet_id)
        form_data = SendForm(request.POST)
        if form_data.is_valid():
          amount = form_data.cleaned_data["amount"]
          address = form_data.cleaned_data["address"]
          wallet.send_to(address , amount , network=network)
          msg = notification.get_message("verify" , amount=amount , address=address , tag=profile_model.tag)
          notification.send(user , user , msg)
        return JsonResponse({"error":form_data.errors})
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
      notification = request.user.notifications.unread()
      return render(request , "wallet/activity/NotificationsActivity.html" , {"notifications":notification})
    return redirect("/havwis/login/")

from Wallet.forms import CountryForm

def debug(request):
  return render(request , "debug.html" , {"country":CountryForm()})

class BuyView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      network_id = kwargs["network_id"]
      trade_object = TradeModel.objects.get(id=network_id)
      return render(request , "wallet/fragment/BuyFragment.html" , {"trade_coin":trade_object})
    return redirect("/auth/login/")
  def post(self , request , *args , **kwargs):
    form_amount_data = IntegerForm(request.POST)
    """Since we are funding virtual card for transaction user dont have to choose transaction type here"""
    #type = TextForm(request.POST)
    if form_amount_data.is_valid():
      customer_id = CustomerModel.objects.get(user=request.user).customer_id
      profile_model = ProfileModel.objects.get(user = request.user)
      customer = flutterwave.card_payment(id , amount , )
      amount = form_amount_data.cleaned_data["number"]
      url = paystack.create_transaction(customer , amount , "payouk.mystre@gmail.com")
      return redirect(url)
      # return HttpResponse(customer)
    trade_object = TradeModel.objects.get(id=network_id)
    return render(request , "wallet/fragment/BuyFragment.html" , {"trade_coin":trade_object})

class SellView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      wallet_id = WalletModel.objects.get(user = request.user).wallet_id
      network = kwargs["network"]
      wallet = Wallet(wallet_id)
      balance = wallet.balance(network=network)
      return render(request , "wallet/fragment/SellFragment.html" , {"network": network , "balance": balance})
    return redirect("/auth/login/")
  def post(self , request , *args , **kwargs):
    if request.user.is_authenticated:
       amount = request.POST["amount"]
       pass