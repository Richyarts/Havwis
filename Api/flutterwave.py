import requests
import json
from Wallet.models import WalletModel , CreditCard
from django.utils import timezone
from .core import flutterwave , key
from harvis.core import generateRandomString as GenerateRandomString
"""
{
  "status": "success",
  "message": "Card fetched successfully",
  "data": {
    "id": "7dc7b98c-7f6d-48f3-9b31-859a145c8085",
    "account_id": 65637,
    "amount": "20,000.00",
    "currency": "NGN",
    "card_hash": "7dc7b98c-7f6d-48f3-9b31-859a145c8085",
    "card_pan": "5366130719043293",
    "masked_pan": "536613*******3293",
    "city": "Lekki",
    "state": "Lagos",
    "address_1": "19, Olubunmi Rotimi",
    "address_2": null,
    "zip_code": "23401",
    "cvv": "267",
    "expiration": "2023-01",
    "send_to": null,
    "bin_check_name": null,
    "card_type": "mastercard",
    "name_on_card": "Jermaine Graham",
    "created_at": "2020-01-17T18:31:48.97Z",
    "is_active": true,
    "callback_url": "https://your-callback-url.com/"
  }
}
"""
apikey = {"authorization":"FLWSECK_TEST-6cf63b691c215e23c3f75c871787f96b-X"}
def CreateCard(user, amount, currency):
    data = {
        "billing_name": user.username, "amount": amount, "currency": currency
        }
    response = requests.post(url = "https://api.flutterwave.com/v3/virtual-cards", headers = apikey , json = data)
    return response.json()["data"]["id"]

def createAccountNumber(user , amount):
  url = "https://api.flutterwave.com/v3/bulk-virtual-account-numbers"
  data = {
    "email":user.email ,
    "amount": amount,
    "is_permanent":False,
  }
  response = requests.post(url=url , headers=apikey , json=data)
  return response.json()["data"]

def createOTP(profile , type):
  customer = {
    "name": profile.user.username ,
    "phone": profile.phone , 
    "email": profile.user.email,
  }
  url = "https://api.flutterwave.com/v3/otps"
  data = {
    "length": 6,
    "send":True,
    "customer": customer,
    "sender": "Havwis",
    "medium":type,
    "expiry":5
  }
  response = requests.post(url=url , headers= apikey , json=data)
  return response.json()["data"][0]["reference"]
  
def verifyOTP(id , otp):
  url = "https://api.flutterwave.com/v3/otps/reference/validate"
  data = {
    "reference":id,
    "otp":otp
  }
  response = requests.post(url=url , headers=apikey , json=data)
  return response.json()
  
def GetCard(id):
    url = "https://api.flutterwave.com/v3/virtual-cards/{0}".format(id)
    response = requests.get(url=url, headers = apikey)
    if response.json()["status"] == "success":
      return {"status":True , "data":response.json()["data"]}
    return {"status":False , "data":response.json()["message"]}

def GetBalance(id):
    url = "https://api.flutterwave.com/v3/virtual-cards/{0}".format(id)
    response = requests.get(url=url, headers = apikey)
    return response.json()["data"]["amount"]

def getTransaction(id):
  #card = GetCard(id)
  url = "https://api.flutterwave.com/v3/virtual-cards/{}/transactions".format(id)
  data = {
    "from":"2021-1",
    "to":timezone.now(),
    "index":0,
    "size":None
  }
  response = requests.get(url=url , headers=apikey , params=data)
  return response.json()

def get_card(request , type):
  if WalletModel.objects.get(user=request.user).credit_card.count() > 0:
    id = WalletModel.objects.get(user=request.user).credit_card.get(label=type).card_id
    return GetCard(id)
  card_id = CreateCard(request.user , "100" , "NGN")
  card = CreditCard.objects.create(card_id = str(card_id) , label = type)
  wallet_model = WalletModel.objects.get(user = request.user).credit_card.add(card)
  return GetCard(card_id)
    
def cardPayment(type , profile , amount , currency):
  card_info = get_card(profile , type)
  card = card_info["data"]
  status = card_info["status"]
  if status:
    date = card["expiration"].split("-")
    if card["is_active"] and float(card["amount"]) > float(0) and float(card["amount"]) >= float(amount):
      payload = {
        "amount": amount, "currency":currency,
        "card_number":card["card_pan"], "cvv":card["cvv"] ,
        "expiry_month":date[1] , "expiry_year":date[0],
        "phone_number": profile.phone , "email": profile.user.email,
        "full_name": profile.user.username , "tx_ref": GenerateRandomString()
      }
      hash_payload = flutterwave.encryptData(key , json.dumps(payload))
      data = { "client":hash_payload }
      url = "https://api.flutterwave.com/v3/charges?type=card"
      response = requests.post(url=url , headers=apikey , json=data)
      if response.json()["status"] != "error":
        return {"status":True , "data":response.json()["data"]}
      return {"status":False , "data":response.json()["message"]}
    return {"status":False , "data":"Low balance! can't process transaction"}
  return {"status":False , "data":card}