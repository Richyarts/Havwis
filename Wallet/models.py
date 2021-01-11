from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime

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
  coin = models.ManyToManyField(CoinModel  , blank=False)
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
 
class NotificationModel(models.Model):
  notificationId = [
    ("security" , "security"),
    ("send" , "send"),
    ("receive" , "receive"),
    ("verify" , "verify"),
  ]
  type = models.CharField(max_length=10 , choices=notificationId)
  text = models.TextField(max_length=500 , blank=False , null=False)
  def __str__(self):
    return self.text
  def get_text(self , type , *args , **kwargs):
    time = naturaltime(timezone.now())
    address = kwargs.get("address")
    amount = kwargs.get("amount")
    network = kwargs.get("network")
    tag = kwargs.get("tag")
    if type == "security":
      return (self.text.format(tag , time))
    if type == "verify":
      return (self.text.format(tag))
    if type == "send":
      return (self.text.format(network , amount , address))
    if type == "receive":
      return (self.text.format(network , amount , address))
    class Meta:
      db_table = "NotificationModel"
      
class TradeModel(models.Model):
  coin_name = models.TextField(max_length = 64 , blank=False , null=False)
  coin_avatar = models.ImageField(upload_to='Authentication/static/market/trade' , blank=False , max_length=500 )
  coin_symbol = models.TextField(max_length = 64 , blank=False , null=False , default="BTC")
  class Meta:
    db_table = "TradeModel"