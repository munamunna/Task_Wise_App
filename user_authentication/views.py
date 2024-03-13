from django.shortcuts import render,redirect
from rest_framework.viewsets import ModelViewSet
from user_authentication.serializers import UserSerializer
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from .models import UserProfile


# views.py

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to TaskWise!")

# Create your views here.
class UsersView(ModelViewSet):
    serializer_class=UserSerializer
    queryset=User.objects.all()
    model=User



def verify_email(request, token):
    # Retrieve the UserProfile associated with the token
    try:
        profile = UserProfile.objects.get(verification_token=token)
    except UserProfile.DoesNotExist:
        # Handle the case where the token is invalid or expired
        return redirect('')  # Redirect to a page indicating an invalid token

    # Mark the user's email as verified (update the UserProfile or User model accordingly)
    profile.user.email_verified = True
    profile.user.save()

    # Redirect the user to a page indicating successful email verification
    print("Redirecting to index view") 
    return redirect('index')





        

    

