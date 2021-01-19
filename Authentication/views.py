import json
from Wallet import send_mail
from bitcoinlib.wallets import wallet_delete
from Authentication.models import ProfileModel , CustomerModel
from django.views import View
from harvis.notifications import notification
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate , login
from Authentication.forms import *
from django.shortcuts import render , redirect
from Wallet.models import WalletModel , CoinModel
from Wallet.wallet import create_wallet
from harvis import paystack
from harvis.core import verify_code , get_tag , generateRandomString #generateRandomString added by Mumeen
from django.contrib.auth.models import User
from django.http import JsonResponse , HttpResponse
from Wallet.forms import CountryForm

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
      send_mail.send_mail_verification(user , self.code)
      #get a random string as suggested by Mummen and signed it with the projects Private key
      unique_id = generateRandomString() 
      #create a wallet  return None if wallet exists -> Have to change that cos of security breach 
      wallet = create_wallet(allow_mnemonic=False , id=unique_id , code=password)
      print(wallet)
      #>>>Wallet return None if failed to create a Wallet check Wallet/wallet.py >>> method create_wallet()
      if wallet != None:
        try:
          #>>>Todo create a form for user to customize profile
          profile_model = ProfileModel.objects.create(user=user , code=self.code , phone=phone , tag=get_tag(username))
          #>>>save the wallet info (Wallet_id) >>>check Wallet/models.py and custom_tags for significant of this instance
          coins = CoinModel.objects.all()
          wallet_model = WalletModel.objects.create(user=user , wallet_id=unique_id)
          #send notification to verify account
          msg = notification.get_message("verify" , tag=profile_model.tag)
          notification.send(user , user , msg)
          for coin_avaliable in coins:
            wallet_model.coin.add(coin_avaliable)
            wallet_model.save()
          #>>>Create a customer instance for paystack payment getaway
          customer_id = paystack.create_customer(user , profile_model)
          customer = CustomerModel(user=user , customer_id=customer_id)
          customer.save()
          user.save()
          return redirect("/auth/verify/{}".format(user.id))
        except:
          wallet_delete(username)
          #>>>To prevent user from being create if there is an error with creating Wallet
          User.objects.get(username=username).delete()
          #>>>return HttpResponse if an error occurs in creating Wallet
          return HttpResponse("<h1>Error creating Wallet </h1>")
      else:
       #>>>To prevent user from being create if there is an error with creating Wallet
       User.objects.get(username=username).delete()
       #>>>return HttpResponse if an error occurs in creating Wallet
       return HttpResponse("<h1>Error creating Wallet </h1>")
    return render(request , 'auth/auth.html' , {"form":form_data.errors , "back_id":"auth-back"})

"""Todo clean up authentication and send_mail to user for email verification"""
class VerificationView(View):
  def get(self , request , *args , **kwargs):
      id = kwargs["id"]
      user = User.objects.get(id = id)
      return render(request , "auth/auth_verify" , {"user":user})
  def post(self , request , *args , **kwargs):
    id = kwargs["id"]
    user = User.objects.get(id = id)
    profile = ProfileModel.objects.get(user=user)
    code = ""
    for codes in range(1 , 7):
      code += request.POST[str(codes)]
    if profile.code == code:
      user.is_active = True
      login(request , user)
      return redirect("/havwis/home/")
    return render(request , "auth/auth_verify" , {"user":user} , {"error":"error"})
 
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
        msg = notification.get_message("security" , tag=username)
        notification.send(user , user , msg)
        login(request , user)
        return redirect("/havwis/home/")
      user = authenticate(email=username , password = password)
      if user is not None:
        login(request , user)
        return redirect("/havwis/home/")       
      return render(request , "auth/login.htm" , {"errors":user , "form":form_data})
    return render(request , "auth/login.htm" , {"errors":form_data.errors , "form":form_data})
    
class ProfileView(View):
  def get(self , request , *args , **kwargs):
    return render(request , "auth/activity/ProfileActivity.html")

class UpdateView(View):
  def get(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      data = None
      type = kwargs["type"]
      if type == "phone":
        data = ProfileModel.objects.get(user = request.user)
        title = "Phone number"
      elif type == "country":
        data = ProfileModel.objects.get(user = request.user)
        title = "Country available"
      else:
        title = "Limits and Features"
      return render(request , "auth/fragment/ProfileFragment.html" , {"update_type":type , "title":title , "data":data})
    return redirect("/auth/login/")
  def post(self , request , *args , **kwargs):
    if request.user.is_authenticated:
      type = kwargs["type"]
      if type == "country":
        form_data = CountryForm(request.POST)
        if form_data.is_valid():
          country = form_data.cleaned_data["country"]
          profile_object = ProfileModel.objects.get(user = request.user)
          profile_object.country = country
          profile_object.save()
          return JsonResponse({"status":True})
        else:
          return JsonResponse({"status":False , "error":form_data.errors})
      elif type == "Phone":
        print("None")
    return redirect("/auth/login/")