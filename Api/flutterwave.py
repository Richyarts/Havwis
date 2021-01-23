import requests
import json
from rave_python import Rave
from harvis.core import generateRandomString
from .core import FlutterwaveHash

test_data = {
  "amount":"1000",
  "currency":"NGN",
  "card_number":"5399670123490229",
  "cvv":"123",
  "expiry_month":"1",
  "expiry_year":"21",
  "email":"user@flw.com",
  "tx_ref": "MC-3243e",
  
}
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
#rave = Rave("FLWPUBK_TEST-b95ed59c15f2726491a0ac88026bb045-X", "FLWSECK_TEST-6cf63b691c215e23c3f75c871787f96b-X", "FLWSECK_TEST4c979cebc80f")
apikey = {"authorization":"FLWSECK_TEST-6cf63b691c215e23c3f75c871787f96b-X"}
def CreateCard(profile, amount, currency):
    data = {
        "billing_name": profile.user.username, "amount": amount, "currency": currency
        }
    response = requests.post(url = "https://api.flutterwave.com/v3/virtual-cards", headers = apikey , json = data)
    return response.json()["data"]["id"]

def GetCard(id):
    url = "https://api.flutterwave.com/v3/virtual-cards/{0}".format(id)
    response = requests.get(url=url, headers = apikey)
    data = response.json()["data"]
    return {"currency":data["currency"] ,"balance":data["amount"] , "card_type":data["card_type"] ,"card_number":data["card_pan"], "cvv":data["cvv"], "expiration":data["expiration"], "card_name":data["name_on_card"]}
    
def GetBalance(id):
    url = "https://api.flutterwave.com/v3/virtual-cards/{0}".format(id)
    response = requests.get(url=url, headers = apikey)
    return response.json()["data"]["amount"]

def get_all_balance(user):
  from Wallet.models import WalletModel
  WalletModel.objects.filter(user = user).credit_card.all()
  balance = 0.0
  for card in cards:
    balance += float(GetBalance(card.card_id))
  return "₦%s"%str(balance)

def card_payment(id , profile , amount):
  card = GetCard(id)
  if float(card["balance"]) > 0 and int(amount) <=float(card["balance"]):
    type = card["card_type"]
    date = card["expiration"].split("-")
    url = "https://api.flutterwave.com/v3/charges?type={}".format("card")
    """data = {
      "amount": amount,
      "currency":card["currency"],
      "card_number": card["card_number"],
      "cvv":card["cvv"],
      "expiry_month":date[1],
      "expiry_year": date[0],
      "email":profile.user.email,
      "tx_ref": generateRandomString(),
      "phone":profile.phone,
      "full_name":profile.user.username,
    }"""
    data = test_data
    hash = FlutterwaveHash()
    sec_key = hash.getKey("FLWSECK_TEST-6cf63b691c215e23c3f75c871787f96b-X")
    hash_data = {"client":hash.encryptData(sec_key , json.dumps(data))}
    response = requests.post(url=url , headers=apikey , json=hash_data)
    print(response.json())
    return response.json()
  return False

def create_account_no(amount , profile):
  url = "https://api.flutterwave.com/v3/virtual-account-numbers"
  data = {
    "email": profile.user.email,
    "amount": amount,
    "tx_ref": generateRandomString(),
    "is_permanent":"true",
  }
  response = request.post(url=url , headers=apikey , json=data)
  print(response.json())
  return response.json()
