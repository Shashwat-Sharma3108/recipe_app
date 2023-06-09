from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTest(TestCase):

    def setUp(self):
        """
            Helper function to test the Superuser login functionality
        """
        self.client = Client()

        #Creating a superuser and then login
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='admin123'
        )
        self.client.force_login(self.admin_user)

        #Creating a normal user and then login
        self.user = get_user_model().objects.create_user(
            email='test123@example.com',
            password='test123'
        )
        self.client.force_login(self.admin_user)

    def test_users_list(self):
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_edit_user_page(self):
        """
            Test user edit page
        """

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
    
    def test_create_user_page(self):
        """
            Test to create user page
        """

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)