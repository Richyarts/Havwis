from django import forms
from django.contrib.auth.models import User
from Authentication.models import ProfileModel , LoginModel

class AuthenticationForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ["email" , "username" , "password" ]
    
class ProfileForm(forms.ModelForm):
  class Meta:
    model = ProfileModel
    fields = '__all__'

class LoginForm(forms.ModelForm):
  class Meta:
    model = LoginModel
    fields = ["username" , "password"]