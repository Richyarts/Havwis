from django.views import View
from django.core import serializers
from django.http import JsonResponse , HttpResponse
from bitcoinlib.wallets import Wallet
from django.shortcuts import render , get_object_or_404
from Wallet.forms import CreditCardForm
from Wallet.models import CoinModel , WalletModel , CreditCard
import json

class JsonSerializable(object):
  def toJson(self):
    return json.dumps(self.__dict__)
  def __repr__(self):
    return self.toJson()
        
class HomeView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/home.htm")
    return redirect("/auth/register/")

class WalletView(View):
  def get(self , request , *args , **kwargs):
    coins = CoinModel.objects.all()
    wallet = WalletModel.objects.filter(user = request.user)
    return render(request , "wallet/wallet.htm" , {"wallets":wallet , "coins":coins})

#>>>Check for wallet_id that user switch to in view and return the wallet object
  def post(self , request , *args , **kwargs):
    wallet_id = request.POST.get("wallet_id")
    if wallet_id != None:
      coins = CoinModel.objects.all()
      wallet = WalletModel.objects.filter(user = request.user)
      wallet_object = Wallet(wallet_id)
      context = {"wallet_object":wallet_object}
      return render(request , "wallet/wallet.htm" , context)
    return JsonResponse(None)
    
class CreditCardView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      return render(request , "wallet/form/credit_card.htm")
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