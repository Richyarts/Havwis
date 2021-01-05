from django.urls import path
from Authentication import views
from rest_framework.routers import DefaultRouter
from Authentication.views import AuthenticationView  , VerificationView, LoginView

urlpatterns = [
   path('register/' , AuthenticationView.as_view() , name="register"),
   path('login/' , LoginView.as_view() , name="login"),
   path('verify/<int:id>' , views.VerificationView.as_view()  , name="verify"),
]