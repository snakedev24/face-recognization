
from django.urls import path
from app import views


urlpatterns = [
  
    path('',views.home,name="home"),
    path('login/',views.user_login , name="user_login"),
    path('signup/', views.signup,name="signup"),
    path('success-login/', views.success_login,name="success_login"),
   
]