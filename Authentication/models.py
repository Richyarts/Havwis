from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

class User(AbstractUser):
  username = models.CharField(unique=True, max_length=12, blank=True, null=True)
  email = models.EmailField(unique=True, blank=False, null=False)
  wallet_id = models.CharField(max_length=32, help_text=_("Use this as wallet identifier"))
  phone_number = models.IntegerField()
  transaction_pin = models.IntegerField(null=True, blank=True)
  avatar =  models.ImageField(upload_to="", default="")
  def __str__(self):
    return self.wallet_id