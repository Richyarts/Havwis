from django.db import models

class CoinModel(models.Model):
  coin_name = models.TextField(max_length = 64 , blank=False , null=False)
  coin_avatar = models.ImageField(upload_to='Authentication/static/user/avatar' , blank=False , max_length=500 )
  class Meta:
    db_table = "CoinModel"