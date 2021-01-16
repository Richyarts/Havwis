from django import forms
from Wallet.models import CreditCard , VirtualCardModel
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

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

class IntegerForm(forms.Form):
  number = forms.IntegerField()

class TextForm(forms.Form):
  text = forms.CharField(max_length=101)

class CountryForm(forms.Form):
  country = CountryField(blank_label='(select country)').formfield()
  class Meta:
    fields = ('name', 'country')
    widgets = {'country': CountrySelectWidget()}