#>>>Written by lyonkvalid 7:40PM Wed , jan 6 2020
import random
from hashlib import sha256

magic_no = [random.randint(0 , 9425)]
magic_no.append(random.randint(0 , 9425))

class GenerateCode:
  def __init__(self):
    self.code = random.randint(magic_no[1] - magic_no[0] , magic_no[1])
       
  def get_code(self):
    return sha256(str(self.code).encode('utf-8')).hexdigest()[:6]
    
def get_tag(value):
  return "@"+value

class VirtualCard():
  def __init__(self , address , city , state , postal_code , country):
    self.address = address
    self.city = city
    self.state = state
    self.postal_code = postal_code
    self.country = country
  def card_holder(self , profile , user):
    return stripe.issuing.CardHolder.create(
      name = "%s %s"%(user.first_name , user.last_name),
      email = user.email,
      phone_number = profile.phone,
      status = "active",
      type = "individual",
      billing = {
        "address":{
          "line1":self.address,
          "city":self.city,
          "state":self.state,
          "postal_code":self.postal_code,
          "country":self.country,
        },
      },
    )
    
  def card(self ,cardholder , currency="usd" , type="virtualcard"):
    return stripe.issuing.Card.create(
      cardholder = cardholder,
      type = type,
    )
verify_code = GenerateCode()
