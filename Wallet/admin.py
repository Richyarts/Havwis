from django.contrib import admin
from Wallet.models import CoinModel , NotificationModel , WalletModel , CreditCard

admin.site.register(CoinModel)
admin.site.register(WalletModel)
admin.site.register(CreditCard)
admin.site.register(NotificationModel)