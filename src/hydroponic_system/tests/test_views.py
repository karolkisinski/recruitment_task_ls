from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from hydroponic_system.models import HydroponicSystem


class HydroponicSystemListCreateTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword')
        self.client.force_authenticate(user=self.user)
        HydroponicSystem.objects.create(
            system_name='Test System', owner=self.user)

    def test_list_hydroponic_systems(self):
        url = reverse('hydroponic-systems')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_hydroponic_system(self):
        url = reverse('hydroponic-systems')
        data = {'system_name': 'New Test System'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 2)

    def tearDown(self):
        User.objects.all().delete()


class HydroponicSystemRetrieveUpdateDestroyTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.system = HydroponicSystem.objects.create(
            system_name='Test System', owner=self.user)

    def test_retrieve_hydroponic_system(self):
        url = reverse('hydroponic-system-api', kwargs={'pk': self.system.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_hydroponic_system(self):
        url = reverse('hydroponic-system-api', kwargs={'pk': self.system.pk})
        data = {'system_name': 'Updated Test System'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.system.refresh_from_db()
        self.assertEqual(self.system.system_name, 'Updated Test System')

    def test_delete_hydroponic_system(self):
        url = reverse('hydroponic-system-api', kwargs={'pk': self.system.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(HydroponicSystem.objects.filter(
            pk=self.system.pk).exists())

    def test_permission_denied(self):
        # Create another user
        another_user = User.objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='testpassword')
        self.client.force_authenticate(user=another_user)
        url = reverse('hydroponic-system-api', kwargs={'pk': self.system.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        User.objects.all().delete()
