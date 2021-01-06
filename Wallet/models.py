from django.db import models
from django.contrib.auth.models import User

class CoinModel(models.Model):
  coin_name = models.TextField(max_length = 64 , blank=False , null=False)
  coin_avatar = models.ImageField(upload_to='Authentication/static/user/avatar' , blank=False , max_length=500 )
  class Meta:
    db_table = "CoinModel"

class CreditCard(models.Model):
  card_type = models.CharField(default="Unknown" , max_length=64)
  card_no =  models.IntegerField()
  card_name = models.CharField(max_length = 64)
  expiry_date = models.DateField()
  cvv = models.IntegerField()
  class Meta:
    db_table = "CreditCard"
    
class WalletModel(models.Model):
  user = models.ForeignKey(User , on_delete=models.CASCADE)
  wallet_id = models.CharField(max_length=64 , blank=False , null=False)
  credit_card = models.ManyToManyField(CreditCard , blank=True)
  balance = models.IntegerField(default=0.00)
  class Meta:
    db_table = "WalletModel"
    
class VirtualCardModel(models.Model):
  user = models.ForeignKey(User , on_delete=models.CASCADE)
  address = models.CharField(max_length=101)
  city = models.CharField(max_length=32)
  state = models.CharField(max_length=32)
  postal_code = models.IntegerField()
  country = models.CharField(max_length=32)
  class Meta:
    db_table = "VirtualCardModel"