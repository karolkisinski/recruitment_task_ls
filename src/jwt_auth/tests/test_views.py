from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class MyTokenObtainPairViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', email='test@example.com',
            password='testpassword')
        self.token_obtain_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        self.client.login(username='testuser', password='testpassword')

    def test_obtain_token_pair(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        refresh_token = RefreshToken.for_user(self.user)
        data = {'refresh': str(refresh_token)}
        response = self.client.post(self.token_refresh_url,
                                    data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
