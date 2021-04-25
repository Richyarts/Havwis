from django import forms

from .models import SendModel

class SendForm(forms.ModelForm):
  class Meta:
    model = SendModel
    fields = ["address", "amount", "network"]