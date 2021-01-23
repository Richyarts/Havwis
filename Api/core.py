import os, hashlib, warnings, requests, json
import base64
from Crypto.Cipher import DES3

class FlutterwaveHash(object):
  def __init__(self):
        pass

  def getKey(self,secret_key):
        hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
        hashedseckeylast12 = hashedseckey[-12:]
        seckeyadjusted = secret_key.replace('FLWSECK-', '')
        seckeyadjustedfirst12 = seckeyadjusted[:12]
        return seckeyadjustedfirst12 + hashedseckeylast12

  def encryptData(self, key, plainText):
        blockSize = 8
        padDiff = blockSize - (len(plainText) % blockSize)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
        test = plainText.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted