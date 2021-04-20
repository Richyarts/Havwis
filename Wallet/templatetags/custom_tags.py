from django import template

from Wallet.models import NetworkDefinition

from Havwis.utils import binance

from bitcoinlib.wallets import Wallet

register = template.Library()

@register.simple_tag
def get_coin_info(request, networks):
  network_info = []
  network_definition = NetworkDefinition.objects.all()
  wallet = Wallet(request.user.wallet_id)
  for network in networks:
    network_info.append({"network":network["network"], "balance":wallet.balance(network=network["network"])})
  return network_info