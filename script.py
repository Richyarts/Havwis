from Wallet.models import NotificationModel

def create_notification(type , text):
  NotificationModel.objects.create(type=type , text=text)

create_notification(type="security" , text="There was a login to your account {0} from a new device on {1}. Review it now.")
create_notification(type="verify" , text="There was a login to your account {0} from a new device on {1}. Review it now.")
create_notification(type="send" , text="There was a login to your account {0} from a new device on {1}. Review it now.")
create_notification(type="receive" , text="There was a login to your account {0} from a new device on {1}. Review it now.")