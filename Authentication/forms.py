from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import User

class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'phone_number', 'email', 'password1', 'password2', )