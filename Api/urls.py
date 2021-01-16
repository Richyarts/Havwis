from django.urls import path
from Api.views import PriceView

urlpatterns = [
  path("price/<ticker>/<int:amount>/" , PriceView.as_view() , name="price"),
]