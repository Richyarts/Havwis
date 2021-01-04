import random
from hashlib import sha256

magic_no = [random.randint(0 , 9425)]
magic_no.append(random.randint(0 , 9425))

class GenerateCode:
  def __init__(self):
    self.code = random.randint(magic_no[0] - magic_no[1] , magic_no[1])
       
  def get_code(self):
    return sha256(str(self.code).encode('utf-8')).hexdigest()[:6]
    
def get_tag(value):
  return "@"+value
  
verify_code = GenerateCode()
