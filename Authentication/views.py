import json
from django.views import View
from django.http import JsonResponse , HttpResponse
from Authentication.forms import *
from django.shortcuts import render
from harvis.core import verify_code , get_tag
from django.contrib.auth.models import User
from Authentication.views import ProfileModel

#Todo add email and phone authentication with verification
class AuthenticationView(View):
  code = verify_code.get_code()
  def get(self , request , *args , **kwargs):
    return render(request , 'auth/auth.html' , {"back_id":"auth-back"})
    
  def post(self , request , *args , **kwargs):
    form_data = AuthenticationForm(request.POST)
    if form_data.is_valid():
      username = form_data.cleaned_data["username"]
      email = form_data.cleaned_data["email"]
      password = form_data.cleaned_data["password"]
      if User.objects.filter(username = username).exists:
        error = {"error":"Username already exists"}
        return JsonResponse(error)
      else:  
        user = User.objects.create_user(username , email , password)
        profile = ProfileModel.objects.create(user=user , code=self.code , phone=phone , tag=get_tag(username))
        user.is_active = False
        user.save()
    return render(request , 'auth/auth.html' , {"form":form_data.errors , "back_id":"auth-back"})

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
      return HttpResponse("<h1>Welcome to Harvis</h1>")
    else:
      return HttpResponse("<h1>Code Error</h1>")
  context = {"error":True}
  JsonResponse(context)
      