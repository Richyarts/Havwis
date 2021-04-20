from binance.client import Client
import time

network_symbols = ["BTC", "LTC", "DASH", "DOGE"]

class Binance():
	def __init__(self):
		self.client = Client("hziRqaoLzBRMlfwULTS66dm527DMVWjF3rQlPJlH5h9kdJwPg4T9MOgeLXYtjhX1", "syLnOpemHBzlyTo2xZEs9vaILt3RNikpdbTHijLFvqaow7HoddxfR3lXgpvRSgVw")
		self.infos = self.client.get_all_tickers()
		
	def get_price(self):
		final_result = []
		for info in self.infos:
		  for symbol in network_symbols:
		    if info["symbol"] == "{}USDT".format(symbol):
		    	final_result.append(info)
		return final_result
	
	def pure_price(self):
	  prices = []
	  for price in self.get_price():
	    price["symbol"] = price["symbol"][:-4]
	    prices.append(price)
	  return prices
	
	def calculate_interest(current_price , last_price):
	  return (current_price - last_price) / last_price * 100
	  
	def get_kline(self, network):
		return binance.client.get_klines(symbol="%sUSDT"%network, interval="1m")
  	
binance = Binance()
