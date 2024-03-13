from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    # Add any other fields you need for the user profile

    def __str__(self):
        return self.user.username
