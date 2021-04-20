from django import template

from Wallet.models import NetworkDefinition

from Havwis.utils import binance

register = template.Library()

@register.simple_tag
def update_price(network, current_price):
  network_definition = NetworkDefinition.objects.get(network=network)
  network_definition.last_price = network_definition.recent_price
  network_definition.recent_price = current_price
  return binance.calculate_interest(float(current_price), network_definition.last_price)