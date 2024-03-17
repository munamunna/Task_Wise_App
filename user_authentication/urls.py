from django.urls import path
from rest_framework.routers import DefaultRouter
from user_authentication.views import UsersView,verify_email
from rest_framework.authtoken.views import ObtainAuthToken

router=DefaultRouter()
router.register("users",UsersView,basename="users")

urlpatterns =[
  
   
     
     path('verify-email/<str:token>/', verify_email, name='verify_email'),
      path('login/', ObtainAuthToken.as_view()),
      
]+router.urls