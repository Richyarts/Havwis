from django.urls import path
from Authentication import views
from Authentication.views import  AuthenticationView  , ProfileView , UpdateView ,  VerificationView, LoginView
from Authentication import views

urlpatterns = [
   path('register/' , AuthenticationView.as_view() , name="register"),
   path('login/' , LoginView.as_view() , name="login"),
   path("logout/" , views.logout_view , name="logout"),
   path('verify/<int:id>/' , views.VerificationView.as_view()  , name="verify"),
   path('profile/' , ProfileView.as_view() , name="profile"),
   path("profile/update/<type>/" , UpdateView.as_view() , name="update"),
] 