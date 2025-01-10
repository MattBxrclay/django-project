from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError 
from django.contrib.auth import get_user_model

class UserModelTests(TestCase):
    def test_create_user(self):
        """Test the creation of a user with email and name"""
        email = "user@example.com"
        name = "User One"
        role = "User"
        user = get_user_model().objects.create_user(
            email=email, name=name, password="password123", role=role
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password("password123"))

    def test_create_user_with_duplicate_email(self):
        """Test that an error is raised when creating a user with a duplicate email"""
        email = "user@example.com"
        name = "User One"
        role = "User"
        get_user_model().objects.create_user(email=email, name=name, password="password123", role=role)

        with self.assertRaises(Exception):
            get_user_model().objects.create_user(email=email, name="User Two", password="newpassword123", role=role)

    def test_create_user_with_invalid_email(self):
        """Test that an invalid email raises a validation error"""
        invalid_email = "invalidemail"
        name = "User One"
        role = "User"

        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(email=invalid_email, name=name, password="password123", role=role)

    def test_password_hashing(self):
        """Test that the user's password are hashed and not stored in plain text"""
        email = "user@example.com"
        name = "User One"
        password = "password123"
        role = "User"
        
        # Create the user
        user = get_user_model().objects.create_user(email=email, name=name, password=password, role=role)
        
        self.assertNotEqual(user.password, password) 
        self.assertTrue(user.check_password(password)) 
