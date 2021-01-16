from django.db import models

class PhoneModel(models.Model):
  country_code = models.IntegerField(primary_key=True)
  country = models.TextField(unique=True)
  is_verify = models.BooleanField(default = False)
  def __str__(self):
    return self.country