from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient, APIRequestFactory
from hydroponic_system.models import HydroponicSystem
from hydroponic_system.serializers import HydroponicSystemSerializer


class HydroponicSystemSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user',
                                             password='test_password')
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_hydroponic_system_serializer_valid_data(self):
        data = {
            'system_name': 'Test System',
            'description': 'Test Description',
        }
        serializer = HydroponicSystemSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_hydroponic_system_serializer_invalid_data(self):
        data = {
            'system_name': '',  # Invalid because system_name is required
            'description': 'Test Description',
        }
        serializer = HydroponicSystemSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_hydroponic_system_serializer_create(self):
        data = {
            'system_name': 'Test System',
            'description': 'Test Description',
        }
        request = self.factory.post('/fake-url/', data)
        request.user = self.user  # Simulate authenticated user

        serializer = HydroponicSystemSerializer(data=data,
                                                context={'request': request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()

        self.assertIsNotNone(instance)
        self.assertEqual(instance.system_name, 'Test System')
        self.assertEqual(instance.description, 'Test Description')
        self.assertEqual(instance.owner, self.user)

    def test_hydroponic_system_serializer_read_only_fields(self):
        hydroponic_system = HydroponicSystem.objects.create(
            system_name='Test System',
            description='Test Description',
            owner=self.user)
        serialized_data = HydroponicSystemSerializer(
            instance=hydroponic_system).data
        self.assertIn('created_at', serialized_data)
        self.assertIn('updated_at', serialized_data)
