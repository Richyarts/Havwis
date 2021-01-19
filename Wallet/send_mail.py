from django.template.loader import render_to_string
from django.core.mail import send_mail
from harvis import settings

def send_mail_verification(user , code):
  string = render_to_string( "verify_mail.html",{ "username": user.username,  "code": code })
  mail = send_mail(subject="Verify Mail" , message=string , html_message=string , from_email=settings.EMAIL_HOST_USER , recipient_list=[user.email] , fail_silently=False)
  print(mail)