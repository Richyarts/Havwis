import random
from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet , BCL_DATABASE_DIR , wallet_exists , wallet_delete
from Wallet.models import WalletModel

def create_wallet(id , allow_mnemonic , code = None):
  if allow_mnemonic:
    mnemonic = Mnemonic().generate()
    if not wallet_exists(id):
      wallet = Wallet.create(id , keys = mnemonic , password=code , network="bitcoin")
      return(wallet , code , mnemonic)
    else:
      return "Wallet already exists"
  wallet = Wallet.create(id , password=code , network="bitcoin")
  return(wallet , code , False)
  
def get_wallet(id):
  return Wallet(id)

def get_backup_wallet(keys):
  pass

def create_new_account(wallet , network):
  return wallet.new_account(network=network)

def get_confirmed_transactions(wallet):
  return wallet.transactions()