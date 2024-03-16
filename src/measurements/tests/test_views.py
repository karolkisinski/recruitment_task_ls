from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from hydroponic_system.models import HydroponicSystem
from measurements.models import Measurements


class HydroponicSystemMeasurementsListCreateTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='password123')
        self.system = HydroponicSystem.objects.create(
            system_name='Test System', owner=self.user)

    def test_list_hydroponic_system_measurements(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = reverse('system_measurements',
                      kwargs={'system_id': self.system.id})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        HydroponicSystem.objects.all().delete()
        User.objects.all().delete()


class Last10MeasurementsListTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='password123')
        self.system = HydroponicSystem.objects.create(
            system_name='Test System', owner=self.user)
        for _ in range(11):
            Measurements.objects.create(hydroponic_system=self.system,
                                        ph=7.0, water_temperature=25.0,
                                        tds=500)

    def test_last_10_measurements(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = reverse('last_10_measurements',
                      kwargs={'system_id': self.system.id})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if the response contains 10 measurements
        self.assertEqual(len(response.data['measurements']), 10)

    def test_last_10_measurements_no_system(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        url = reverse('last_10_measurements', kwargs={'system_id': 9999})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_last_10_measurements_unauthorized_user(self):
        other_user = User.objects.create_user(username='other_user',
                                              password='password123')
        client = APIClient()
        client.force_authenticate(user=other_user)
        url = reverse('last_10_measurements',
                      kwargs={'system_id': self.system.id})
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def tearDown(self):
        HydroponicSystem.objects.all().delete()
        Measurements.objects.all().delete()
        User.objects.all().delete()
