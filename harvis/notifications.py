from notifications.signals import notify
from Wallet.models import NotificationModel
from django.contrib.auth.models import User

class Notification():
  def __init__(self , *args , **kwargs):
    pass
  def send(self , admin , user, message):
    notification = notify.send(admin , recipient=user , verb=message)
    return notification
  def get_message(self , type , *args , **kwargs):
    return NotificationModel.objects.get(type=type).get_text(type=type , **kwargs)

notification = Notification()