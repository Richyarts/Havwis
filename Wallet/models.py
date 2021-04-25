from django.db import models
from django.utils import timezone

from Authentication.models import User

class NetworkDefinition(models.Model):
  network = models.TextField()
  symbol = models.TextField()
  avatar = models.ImageField(upload_to="Static/network/.thumbnails/")

class SendModel(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
  receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE, blank=True, null=True)
  network = models.CharField(max_length=16)
  amount = models.FloatField()
  address = models.CharField(max_length=64)
  is_verify = models.BooleanField(default=False)
  description = models.TextField(blank=True)
  date_added = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return self.sender.username
  class Meta:
    ordering = ["-date_added"]