from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

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


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='Test User Full Name',
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)


    def test_user_page_change(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)