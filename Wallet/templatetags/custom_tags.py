from django import template
register = template.Library()

from Wallet.wallet import *
from bitcoinlib.wallets import *
from bitcoinlib.networks import *

@register.simple_tag
def get_balance(id , network):
  return print_value(int(Wallet(id).balance(network=network)) , network = network)

from Wallet.models import WalletModel

@register.simple_tag
def get_user_wallets(user):
  if WalletModel.objects.filter(user = user).exists:
    return WalletModel.objects.filter(user = user)
  return None

@register.simple_tag
def get_wallet_id(wallet):
  return Wallet.wallet_id

@register.simple_tag
def get_wallet(wallet_id):
  return Wallet()

@register.simple_tag
def create_new_account(network , id):
  try:
    new_wallet = Wallet(id).new_account(network=network)
    return new_wallet
  except:
    return None
    
@register.simple_tag
def delete_model_object(model):
  try:
    model.delete()
    return True
  except:
    return False

@register.simple_tag
def get_wallet_instance(wallet_name):
  try:
    return Wallet(wallet_name)
  except:
    return wallet_name

@register.simple_tag
def card_no_format(value):
  value = str(value)
  return "{0} {1}  {2}  {3}".format(value[:4] , value[4:][:4] , value[8:][:4] , value[12:][:4])
  
@register.simple_tag
def get_cards(wallet):
  return wallet.credit_card.all