from django import template

from Wallet.models import NetworkDefinition

from Havwis.utils import binance

from bitcoinlib.wallets import Wallet
from bitcoinlib.networks import print_value

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
        print(info["symbol"])
        balance += float(info["priceUsd"]) * float(wallet.balance(network=network.network))
  return balance

import os , sys

@register.simple_tag
def get_balance_differ(request, infos):
  new_balance = total_balance(request, infos)
  last_balance = 0
  path ="/Static/price_differ_{}".format(request.user.username)
  if os.path.exists(path):
    with open(path, "r") as file:
      last_balance = float(file.read())
      file.close()
    with open(path, "w") as file:
      file.write(new_balance)
      file.close()
    interest = new_balance - last_balance
    if interest > 0:
      return {"interest":"+{}".format(interest), "percentInterest": interest/last_balance*100}
    else:
      return {"interest":"-{}".format(interest), "percentInterest": interest/last_balance*100}
  else:
    file = open("/Static/price_differ_{}.txt".format(request.user.username), "w")