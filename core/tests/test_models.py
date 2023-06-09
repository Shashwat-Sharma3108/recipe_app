"""
    Tests for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTest(TestCase):
    """
        Testing Models
    """

    def test_create_user_with_email_successful(self):

        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@EXAMPLE.com','Test2@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'testing@123')
            self.assertEqual(user.email, expected)
    
    def test_new_user_without_email_raises_error(self):
        
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','test123')
        
    def test_create_super_user(self):
        """
            Test for creating Super User
        """

        user = get_user_model().objects.create_superuser(
            'test123@example.com',
            'super123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)