from django.contrib.auth.models import User
from Wallet.models import WalletModel
from bitcoinlib.wallets import Wallet

class Trade(object):
  def __init__(self , id , amount , *args , **kwargs):
    self.id = id
    self.amount = amount
    
  def getSuperUser(self , username):
    return User.objects.get(username=username)
    
  def buy(self , request , status , network):
    if status:
      super_user = getSuperUser("havwis")
      vendor_wallet_id = WalletModel.objects.get(user = super_user).wallet_id
      user_wallet_id = WalletModel.objects.get(user = request.user).wallet_id
      vendor_wallet = Wallet(vendor_wallet_id)
      user_wallet = Wallet(user_wallet_id)
      user_network_address = user_wallet.get_key(network=network).address
      tx_info = vendor_wallet.send_to(address = user_network_address , amount=self.amount , network=network)
      return {"status":True , "info":tx_info}
    else:
      return {"status":False , "info":failed}
      
  def buy(self , request , status , network):
    if status:
      super_user = getSuperUser("havwis")
      vendor_wallet_id = WalletModel.objects.get(user = super_user).wallet_id
      user_wallet_id = WalletModel.objects.get(user = request.user).wallet_id
      vendor_wallet = Wallet(vendor_wallet_id)
      user_wallet = Wallet(user_wallet_id)
      vendor_network_address = vendor_wallet.get_key(network=network).address
      tx_info = user_wallet.send_to(address = vendor_network_address , amount=self.amount , network=network)
      return {"status":True , "info":tx_info}
    else:
      return {"status":False , "info":failed}
      