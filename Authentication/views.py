import json
from django.views import View
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate , login
from Authentication.forms import *
from django.shortcuts import render , redirect
from Wallet.models import WalletModel
from Wallet.wallet import create_wallet
from harvis.core import verify_code , get_tag
from django.contrib.auth.models import User
from Authentication.views import ProfileModel
from django.http import JsonResponse , HttpResponse

""""
    Writing by Lyonkvalid http://github.com/lyonkvalid @2.12AM Tue , JAN 15
    >>>Get the sign up page - html file: ./Authentication/templates/auth/auth.html
    >>>Create a user instance via post request and save data respectively , check ProfileModel , WalletModel
"""

class AuthenticationView(View):
  #>>>OTP code request and save in profile model on request for verification by user
  code = verify_code.get_code()
  def get(self , request , *args , **kwargs):
    return render(request , 'auth/auth.html' , {"back_id":"auth-back"})
    
  def post(self , request , *args , **kwargs):
    form_data = AuthenticationForm(request.POST)
    if form_data.is_valid():
      """
      >>>User fields [username , email , password]
      >>>Todo add custom Field and Auth Email , phone or token later in future
      """
      username = form_data.cleaned_data["username"]
      email = form_data.cleaned_data["email"]
      password = form_data.cleaned_data["password"]
      #Todo add phone field to UserModel and sending OTP code view phone
      phone = request.POST["phone"]
      #Create a user instance and set user.is_active{false} cos user haven't verify email
      user = User.objects.create_user(username , email , password)
      user.is_active = False
      #get a random string as suggested by Mummen and signed it with the projects Private key
      unique_id = Signer.sign(get_random_string(length=64))
      #create a wallet  return None if wallet exists -> Have to change that cos of security breach 
      wallet = create_wallet(allow_mnemonic=False , id=unique_id , code=password)
      print(wallet)
      #>>>Wallet return None if failed to create a Wallet check Wallet/wallet.py >>> method create_wallet()
      if wallet != None:
        #>>>Todo create a form for uset to customize profile
        profile_model = ProfileModel.objects.create(user=user , code=self.code , phone=phone , tag=get_tag(username))
        #>>>save the wallet info (Wallet_id) >>>check Wallet/models.py and custom_tags for significant of this instance
        coins = CoinModel.objects.all()
        wallet_model = WalletModel.objects.create(user=user , wallet_id=unique_id)
        for coin_avaliable in coins:
          wallet_model.coin.add(coin_avaliable)
          wallet_model.save()
        user.save()
        return redirect("/auth/login/")
      else:
       #>>>To prevent user from being create if there is an error with creating Wallet
       User.objects.get(username=username).delete()
       #>>>return HttpResponse if an error occurs in creating Wallet
       return HttpResponse("<h1>Error creating Wallet </h1>")
    return render(request , 'auth/auth.html' , {"form":form_data.errors , "back_id":"auth-back"})

"""Todo clean up authentication and send_mail to user for email verification"""
class VerificationView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      id = kwargs["id"]
      user = User.objects.get(id = id)
      return render(request , "auth/auth_verify" , {"user":user})
    return redirect("/auth/register/")
    
  def post(request):
    profile = ProfileModel.objects.get(user = request.user)
    code_value = []
    code = ""
    for x in range(1 , 6):
      code_value.append(request.POST["code"+x])
    for x in code_value:
      code += x
    if code == profile.code:
      return HttpResponse("<h1>Welcome to havwis</h1>")
    else:
      return HttpResponse("<h1>Code Error</h1>")
  context = {"error":True}
  JsonResponse(context)

class LoginView(View):
  def get(self , request , *args , **kwargs):
    return render(request , "auth/login.htm")
  def post(self , request , *args , **kwargs):
    form_data = LoginForm(request.POST)
    if form_data.is_valid():
      username = request.POST["username"]
      password = request.POST["password"]
      user = authenticate(username=username , password = password)
      if user is not None:
        login(request , user)
        return redirect("/havwis/home/")
      user = authenticate(email=username , password = password)
      if user is not None:
        login(request , user)
        return redirect("/havwis/home/")       
      return render(request , "auth/login.htm" , {"errors":user , "form":form_data})
    return render(request , "auth/login.htm" , {"errors":form_data.errors , "form":form_data})
    