from django.shortcuts import render
from harvis.core import get_price
from django.http import JsonResponse
from django.views import View

class PriceView(View):
  def get(self , request , *args , **kwargs):
    ticker = kwargs.get("ticker")
    amount = kwargs.get("amount")
    return JsonResponse(get_price(ticker , amount) , safe=False)