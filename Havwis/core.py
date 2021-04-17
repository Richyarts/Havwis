#last updated by @lyonkvalid

#check the Authentication models , updated the custom User object 
#>>>might be deprecated in future
from Authentication.models import User

#import bitcoinlib module 
#>>>check bitcoinlib documentation for reference
from bitcoinlib.wallets import Wallet, wallet_delete, wallet_exists

from .settings import DEBUG

NETWORK = ["bitcoin", "litecoin", "dash", "dogecoin"]
NETWORK_TEST = ["testnet", "litecoin_testnet", "dash_testnet", "dogecoin_testnet", ]

class HavwisCryptoWallet():
  def __init__(self, request=None, user=None):
    self.user = request.user if request is not None else user
    self.networks = NETWORK if not DEBUG else NETWORK_TEST
    
  def get_wallet(self):
    wallet_id = self.user.wallet_id
    if wallet_exists(wallet_id):
      return Wallet(wallet_id)
  
  def create_wallet(self, create_wallet_id):
      wallet = Wallet.create(create_wallet_id, network=self.networks[0])
      for network in self.networks:
        if network != self.networks[0]:
          wallet.new_account("%s wallet"%network, network=network)
      return wallet
        
  def update_wallet(self):
    wallet = self.get_wallet()
    for network in self.networks:
      wallet.utxos_update()
      wallet.scan(network=network)
    return {"status": True}
  
  def get_address(self, network):
    return self.get_wallet().get_key(network=network).address
  
  def get_balance(self, network):
    return self.get_wallet().balance(network=network)

class HavwisTransaction():
  def __init__(self, wallet, network, amount, address):
    self.wallet = wallet
    self.network = network
    self.amount = amount
    self.address = address
  
  def send(self):
    try:
      tx_object = self.wallet.send_to(self.address, self.amount, network=self.network)
      return {"status":True, "data":{"tx_id":str(tx_object)}}
    except:
      return {"status":False, "data":{"err":e}}

  def get_transaction_fee(self):
    try:
      tx_object = self.wallet.send_to(self.address, self.amount, network=self.network, offline=True)
      return {"status":True, "data":{"fee":tx_object.fee}}
    except exception as e:
      return {"status":False, "data":{"err":e}}