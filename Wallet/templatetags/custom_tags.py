from django import template
from coinmarketcapapi import CoinMarketCapAPI, CoinMarketCapAPIError
register = template.Library()

from Wallet.wallet import *
from bitcoinlib.networks import *
from bitcoinlib.wallets import *
from bitcoinlib.networks import *

cmc = CoinMarketCapAPI('5fec81c9-dc6b-45dd-82ea-c86d7615adbb')

@register.simple_tag
def get_balance(id , network):
  symbol = NETWORK_DEFINITIONS[network]["currency_code"]
  amount = int(Wallet(id).balance(network=network))
  if amount > 0:
    return "${0}".format (cmc.tools_priceconversion(symbol=symbol ,  amount=amount))
  return "$0.00"

@register.simple_tag
def currency_symbol(network):
  return NETWORK_DEFINITIONS[network]["currency_code"]
  
from Wallet.models import WalletModel

@register.simple_tag
def get_user_wallets(user):
  if WalletModel.objects.filter(user = user).exists:
    return WalletModel.objects.filter(user = user)
  return None

@register.simple_tag
def get_wallet_id(wallet):
  return Wallet.wallet_id[:4]

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
  return "{0} {1}  {2}  {3}".format("****" , "****" , "****" , value[12:][:4])
  
@register.simple_tag
def get_cards(wallet):
  return wallet.credit_card.all