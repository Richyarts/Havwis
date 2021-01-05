from django import forms
from Wallet.models import CreditCard

class CreditCardForm(forms.ModelForm):
  class Meta:
    model = CreditCard
    fields = ["card_no" ,"card_name" , "expiry_date" , "cvv"]