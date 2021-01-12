from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.conf import settings 
from paystackapi.verification import Verification 
from django_countries.fields import CountryField

class ProfileModel(models.Model):
  code = models.CharField(max_length = 6 , blank=False)
  user = models.OneToOneField(User , on_delete=models.CASCADE)
  phone = models.IntegerField(blank=True , null=True)
  avatar = models.ImageField(upload_to='Authentication/static/user/avatar' , blank=True , max_length=500 )
  bio = models.CharField(max_length=101)
  tag = models.CharField(max_length = 32 , unique=True , blank=False)
  location = CountryField(default="NGN")
  def __str__(self):
    return (str(user) , id)
  def verify_phone(sender , instance , created , **kwargs):
    response = Verification.verify_phone(
      verify_type="truecaller",
      phone = self.phone,
      callback_url = "http://127.0.0.1:8000/auth/verify/{0}/".format(self.user.id)
    )
    instance.save()
  pre_save.connect(verify_phone , sender=ProfileModel)
  class Meta:
    db_table= "ProfileModel"
  
class LoginModel(models.Model):
  username = models.CharField(max_length=32)
  password = models.CharField(max_length=32)

class CustomerModel(models.Model):
  user = models.OneToOneField(User , on_delete=models.CASCADE)
  customer_id = models.CharField(max_length=64)
  def __str__(self):
    return (str(user) , customer_id)