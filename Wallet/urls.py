from django.urls import path

from .views import SendView

urlpatterns = [
  path("send/", SendView.as_view(), name="send"),
]