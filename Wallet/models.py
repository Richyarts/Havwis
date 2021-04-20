from django.db import models

class NetworkDefinition(models.Model):
  network = models.TextField()
  symbol = models.TextField()
  avatar = models.ImageField(upload_to="Static/network/.thumbnails/")
  recent_price = models.FloatField()
  last_price = models.FloatField()