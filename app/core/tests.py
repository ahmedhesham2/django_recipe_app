from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'ahmed_hesham99@outlook.com'
        passoword = 'admin'
        testuser = get_user_model().objects.create_user(email,passoword)
        self.assertEqual(testuser.email , email)
        self.assertTrue(testuser.check_password(passoword))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'm.hesham@OUTLOOK.COM'
        password = 'test'
        testuser = get_user_model().objects.create_user(email,password)
        self.assertEqual(testuser.email  , email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        email = 'test@test.com'
        password = 'password'
        testsuperuser = get_user_model().objects.create_superuser(email,password)
        self.assertTrue(testsuperuser.is_staff)
        self.assertTrue(testsuperuser.is_superuser)
