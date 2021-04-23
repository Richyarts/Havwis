#last update by @lyonkvalid

from binance.client import Client
from binance.websockets import BinanceSocketManager

import time
import requests

class Flutterwave():
  def __init__(self, api_key):
    self.base_url = "https://api.flutterwave.com/v3/"
    self.api_key = api_key
    self.Authorization = {"Authorization":api_key}
  
  """
    param customer: {name, phone_number, email},
    type customer: dict,
  """
  def create_otp(self, length=6, customer={}, expiry=5):
    data = {
      "sender":"Havwis",
      "length":length,
      "customer":customer,
      "medium":["sms", "whatsapp", "email"],
      "expiry":expiry,
    }
    response_object = request.post(base_url+"otps", headers=Authorization, json=data)
    return {"status":True, "data":response_object.json()}
  
  def validate_otp(reference, otp):
    data = {
      "reference":reference,
      "otp":otp,
    }
    response_object = request.post(base_url+"reference/validate", headers=Authorization, json=data)
    return {"status":True, "data":response_object.json()}

#initialize Flutterwave 
flutterwave = Flutterwave(None)

network_symbols = ["BTC", "LTC", "DASH", "DOGE"]

def manager(msg):
  print(msg)

process_message = manager()

class Binance():
  def __init__(self):
    self.client = Client("hziRqaoLzBRMlfwULTS66dm527DMVWjF3rQlPJlH5h9kdJwPg4T9MOgeLXYtjhX1", "syLnOpemHBzlyTo2xZEs9vaILt3RNikpdbTHijLFvqaow7HoddxfR3lXgpvRSgVw")

  def get_price(self):
    infos = self.client.get_ticker()
    final_result = []
    for info in infos:
      for symbol in network_symbols:
        if info["symbol"] == "{}USDT".format(symbol):
          final_result.append(info)
    return final_result

  def pure_price(self):
    prices = self.get_price()
    final_result = []
    for price in prices:
      price["symbol"] = price["symbol"][:-4]
      final_result.append(price)
    return final_result
	  
  def get_kline(self, network):
    return binance.client.get_klines(symbol="%sUSDT"%network, interval="1m")
  
  def socket_get_price(self):
    global process_message
    binance = Binance()
    binance_socket= BinanceSocketManager(binance.client)
    binance_socket.start_ticker_socket(process_message)
    
  
#initialize Binance
try:
  binance = Binance()
  manager = BinanceSocketManager(binance.client)
  manager.start_ticker_socket(process_message)
except:
  binance = None