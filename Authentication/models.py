from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 


class ProfileModel(models.Model):
  code = models.CharField(max_length = 6 , blank=False)
  user = models.OneToOneField(User , on_delete=models.CASCADE)
  phone = models.IntegerField(blank=True , null=True)
  avatar = models.ImageField(upload_to='Authentication/static/user/avatar' , blank=True , max_length=500 )
  bio = models.CharField(max_length=101)
  tag = models.CharField(max_length = 32 , unique=True , blank=False)
  location = models.CharField(max_length=64)
  class Meta:
    db_table= "ProfileModel"

class LoginModel(models.Model):
  username = models.CharField(max_length=32)
  password = models.CharField(max_length=32)