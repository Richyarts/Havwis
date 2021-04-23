import shrimpy

# An unofficial wrapper for shrimpy written by @lyonkvalid
class HavwisShrimpyGetaway():
	def __init__(self):
		self.public_key = '1504fc9bbc22378f703bd6dfb7ca1d8f2cbdfabc67748689285d420d1324d18e'
		self.private_key = 'f99e4918a855c67faedeebc3f83425a9d727eda2cd70d806f26f0746ba74855e85a633ae10b46973a3b2bf452702b505f859e769cef9e1f7bfe5196bdcbcb490'
		self.client = shrimpy.ShrimpyApiClient(self.public_key, self.private_key)
	
  #returns ticker price lists	
	def getCryptoPrices(self):
		return self.client.get_ticker('binance')

import ccxt

class HavwisDashBoard():
	def __init__(self):
		self.exchange_id = 'binance'
		self.exchange_class = getattr(ccxt, self.exchange_id)
		self.exchange = self.exchange_class({
		  'apiKey':'',
		  'secret':'',
		  'enableRateLimit':True,
		})
	'''
    method calculateTxFee: calculate transaction fee,
    returns float: amount in standard currency conversion
  '''
	def calculateTxFee(self, market):
		exchange = ccxt.Exchange({
		  'id':self.exchange_id,
		  'markets':{'BTC/USDT': market},
		})
		return exchange.calculate_fee("BTC/USDT", 'limit', 'sell', 1000, 1000, 'taker', {})