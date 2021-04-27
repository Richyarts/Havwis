from django.db import models
from django.utils import timezone

from Authentication.models import User

class NetworkDefinition(models.Model):
  network = models.TextField()
  symbol = models.TextField()
  avatar = models.ImageField(upload_to="Static/network/.thumbnails/")
  fee = models.FloatField()

class SendModel(models.Model):
  sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
  receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE, blank=True, null=True)
  network = models.CharField(max_length=16)
  amount = models.FloatField()
  address = models.CharField(max_length=64)
  tx_id = models.CharField(blank=True, max_length=64)
  is_verify = models.BooleanField(default=False)
  description = models.TextField(blank=True)
  date_added = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return self.sender.username
  class Meta:
    ordering = ["-date_added"]

class NotificationModel(models.Model):
  notificationId = [
    ("security" , "security"),
    ("send" , "send"),
    ("receive" , "receive"),
    ("verify" , "verify"),
    ("create" , "create"),
  ]
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  type = models.CharField(max_length=10 , choices=notificationId)
  header = models.TextField()
  number = models.FloatField(null=True, blank=True)
  text = models.TextField(max_length=500 , blank=False , null=False)
  date_added = models.DateTimeField(default=timezone.now)
  def __str__(self):
    return self.user.username