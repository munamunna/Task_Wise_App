from django.test import TestCase
from django.contrib.auth.models import User
from user_authentication.serializers import UserSerializer
from unittest.mock import patch


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.validated_data = {
            "username": "muna",
            "email": "munapm1@gmail.com",
            "password": "Password123"
        }

    
    
    
    def test_validate_email_already_exists(self):
        # Create a user with the same email as in the validated_data
        existing_user = User.objects.create_user(username='muna', email='munapm1@gmail.com', password='Password123')
        
        serializer = UserSerializer(data=self.validated_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertEqual(serializer.errors['email'][0], "Email address already exists.")

    
    
