from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'testuser@example.com',
            'full_name': 'Test User',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_new_user(self):
        data = {
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'password': 'newpassword123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User registered successfully')



    def test_login_valid_credentials(self):
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword123'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)
        self.assertEqual(response.data['detail'], 'User logged in successfully')

