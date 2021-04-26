from django import template

from Wallet.models import NetworkDefinition

from Havwis.utils import Binance

from bitcoinlib.wallets import Wallet
from bitcoinlib.networks import print_value, NETWORK_DEFINITIONS

register = template.Library()

@register.simple_tag
def get_networks_info(request, networks):
  network_infos = []
  wallet = Wallet(request.user.wallet_id)
  for network in networks:
    network_info.append({"network":network["network"], "balance":wallet.balance(network=network["network"])})
  return network_infos

@register.simple_tag
def get_balance_network_usd(request, network, usd_price):
  wallet = Wallet(request.user.wallet_id)
  balance_in_satoshi = wallet.balance(network=network)
  balance_in_bitcoin = balance_in_satoshi/1000000
  price_in_usd = float(balance_in_bitcoin) * float(usd_price)
  return {"priceUSD":price_in_usd, "balanceBTC":print_value(balance_in_bitcoin, network=network.lower())}

@register.simple_tag
def get_balance(request, network):
  return Wallet(request.user.wallet_id).balance(network=network)

@register.simple_tag
def total_balance(request, infos):
  wallet = Wallet(request.user.wallet_id)
  networks = NetworkDefinition.objects.all()
  balance = 0
  for info in infos:
    for network in networks:
      if info["symbol"] == network.symbol:
        balance += float(info["priceUsd"]) * float(wallet.balance(network=network.network))
  return balance

import os , sys

@register.simple_tag
def get_balance_differ(request, infos):
  new_balance = total_balance(request, infos)
  last_balance = request.session.get("last_balance")
  if last_balance is not None:
    interest = new_balance - last_balance
    request.session["last_balance"] = new_balance
    if interest > 0:
      return {"interest":interest, "percentInterest": interest/last_balance}
    else:
      try:
        return {"interest":interest, "percentInterest": interest/last_balance}
      except:
        return {"interest":interest, "percentInterest": "0.00"}
  else:
    request.session["last_balance"] = new_balance
    return {"interest":new_balance, "percentInterest":0.00 }

@register.simple_tag
def print_network_value(network, value):
  return print_value(value, network=network)

@register.filter(name="code")
def code(network):
  return NETWORK_DEFINITIONS[network]["currency_code"]

@register.filter(name="to_float")
def to_float(value):
  return float(value)