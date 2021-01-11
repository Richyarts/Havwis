from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction
from paystackapi.customer import Customer

paystack_secret = "sk_test_30b6ca900a4c68ce92fcce2b92f5eb26f9d20ca0"

paystack = Paystack(secret_key=paystack_secret)


def create_transaction(customer , amount , email):
  transaction = Transaction.initialize(
    amount = amount ,
    email = email ,
    customer = customer,
  )
  return transaction["data"]["authorization_url"]

def create_customer(user , profile):
  customer = Customer.create(
    first_name = user.first_name , last_name= user.last_name ,
    email = user.email , phone=profile.phone
  )
  return customer["data"]["customer_code"]

def get_customer(id):
  customer = Customer.get(customer_id=id)
  return customer