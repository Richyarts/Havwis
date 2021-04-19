#last update by @lyonkvalid

import requests

class Flutterwave ():
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
      "reference":reference,
      "otp":otp,
    }
    response_object = request.post(base_url+"reference/validate", headers=Authorization, json=data)
    return {"status":True, "data":response_object.json()}
  