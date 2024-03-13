from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.authtoken.models import Token

from django.conf import settings
import secrets

from .models import UserProfile

def generate_verification_token(user):
    # Generate a random token using the secrets module
    token = secrets.token_urlsafe(32)
    # Create or update the user's profile with the verification token
    profile, created = UserProfile.objects.get_or_create(user=user)
    profile.verification_token = token
    profile.save()
    return token


class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.send_verification_email(user)
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email address already exists.")
        return value
    def send_verification_email(self, user):
        token = generate_verification_token(user)
        verification_url = reverse('verify_email', kwargs={'token': token})
        full_verification_url = settings.BASE_URL + verification_url

        subject = 'Email Verification'
        context = {'verification_url': full_verification_url}
        html_message = render_to_string('verification_email_template.html', context)
        plain_message = strip_tags(html_message)  # Strip HTML tags for plain text version
        from_email = settings.EMAIL_HOST_USER
        to_email = [user.email]
        
        send_mail(subject, plain_message, from_email, to_email, html_message=html_message)




