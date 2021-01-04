from django.urls import path
from Authentication import views
from rest_framework.routers import DefaultRouter
from Authentication.views import AuthenticationView  , VerificationView

urlpatterns = [
   path('register/' , AuthenticationView.as_view() , name="register"),
   path('verify/<int:id>' , views.VerificationView.as_view()  , name="verify"),
]