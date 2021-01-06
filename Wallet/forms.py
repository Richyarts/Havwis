from django import forms
from Wallet.models import CreditCard , VirtualCardModel

class CreditCardForm(forms.ModelForm):
  class Meta:
    model = CreditCard
    fields = ["card_no" ,"card_name" , "expiry_date" , "cvv"]

class VirtualCardForm(forms.ModelForm):
  class Meta:
    model = VirtualCardModel
    fields = ["address" , "city" , "state" , "postal_code" , "country"]

class SendForm(forms.Form):
  amount = forms.IntegerField()
  address = forms.CharField(max_length=64)