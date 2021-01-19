from django import forms
from Wallet.models import CreditCard , VirtualCardModel
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

class CreditCardForm(forms.ModelForm):
  card_no = forms.IntegerField()
  card_name = forms.CharField(max_length=64)
  expiry_date = forms.DateField()
  cvv = forms.IntegerField()

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