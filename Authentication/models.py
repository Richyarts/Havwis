from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class User(AbstractUser):
  wallet_id = models.CharField(max_length=32, help_text=_("Use this as wallet identifier"))
  phone_number = None
  transaction_pin = models.IntegerField()
  avatar =  models.ImageField(upload_to="", default="")
  def __str__(self):
    return self.wallet_id