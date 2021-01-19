import requests
import json
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
def CreateCard(user, profile, amount, currency):
    data = {
        "billing_name": user.username, "amount": amount, "currency": currency
        }
    response = requests.post(url = "https://api.flutterwave.com/v3/virtual-cards", headers = apikey , json = data)
    return response.json()["data"]["id"]

def GetCard(id):
    url = "https://api.flutterwave.com/v3/virtual-cards/{0}".format(id)
    response = requests.get(url=url, headers = apikey)
    data = response.json()["data"]
    return {"card_type":data["card_type"] ,"card_number":data["card_pan"], "cvv":data["cvv"], "expiration":data["expiration"], "card_name":data["name_on_card"]}
    
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