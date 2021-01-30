from django.contrib.auth.models import User
from Authentication.models import ProfileModel
from Api import flutterwave

user = User.objects.get(username="payouk")
profile = ProfileModel.objects.get(user=user)
pay = flutterwave.cardPayment("trade" , profile , "50" , "NGN")