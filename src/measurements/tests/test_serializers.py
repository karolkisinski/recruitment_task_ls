import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from hydroponic_system.models import HydroponicSystem
from measurements.models import Measurements
from measurements.serializers import MeasurementsSerializer, SystemMeasurementsSerializer, CombinedSerializer # noqa
from rest_framework.exceptions import ValidationError


class SerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpassword')
        self.system = HydroponicSystem.objects.create(
            system_name='Test System', owner=self.user)
        self.measurement = Measurements.objects.create(
            hydroponic_system=self.system,
            ph=6.5,
            water_temperature=25.0,
            tds=500,
        )

    def test_measurements_serializer(self):
        serializer = MeasurementsSerializer(instance=self.measurement)
        expected_data = {
            'id': self.measurement.id,
            'ph': 6.5,
            'water_temperature': 25.0,
            'tds': 500,
            'date': self.measurement.date.strftime(
                '%Y-%m-%dT%H:%M:%S.%f') + 'Z'
        }
        self.assertEqual(serializer.data, expected_data)

    def test_system_measurements_serializer(self):
        serializer = SystemMeasurementsSerializer(instance=self.system)
        expected_data = {
            'id': self.system.id,
            'system_name': 'Test System',
            'measurements': [
                {
                    'id': self.measurement.id,
                    'ph': 6.5,
                    'water_temperature': 25.0,
                    'tds': 500,
                    'date': self.measurement.date.strftime(
                        '%Y-%m-%dT%H:%M:%S.%f') + 'Z'
                }
            ]
        }

        self.assertEqual(serializer.data, expected_data)

    def test_combined_serializer(self):
        serializer = CombinedSerializer({
            'system': self.system,
            'measurements': [self.measurement]
        })
        serialized_data = json.loads(json.dumps(serializer.data))
        expected_data = {
            'system': {
                'system_name': 'Test System',
                'description': None,
                'created_at': self.system.created_at.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f') + 'Z',
                'updated_at': self.system.updated_at.strftime(
                    '%Y-%m-%dT%H:%M:%S.%f') + 'Z'
            },
            'measurements': [
                {
                    'id': self.measurement.id,
                    'ph': 6.5,
                    'water_temperature': 25.0,
                    'tds': 500,
                    'date': self.measurement.date.strftime(
                        '%Y-%m-%dT%H:%M:%S.%f') + 'Z'
                }
            ]
        }
        self.assertEqual(serialized_data, expected_data)


class SerializerNegativeTests(TestCase):

    def test_invalid_measurement_serializer(self):
        invalid_data = {
            'ph': 'invalid_ph',
            'water_temperature': 25.0,
            'tds': 500,
            'date': 'invalid_date',
        }
        serializer = MeasurementsSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_system_measurements_serializer(self):
        invalid_data = {
            'system_name': 'Test System',
            'measurements': [{'invalid_key': 'invalid_value'}]
        }
        serializer = SystemMeasurementsSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_invalid_combined_serializer(self):
        invalid_data = {
            'system': {'id': 1},  # Missing 'system_name'
            'measurements': [{'ph': 6.5}]  # Missing required fields
        }
        serializer = CombinedSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

        invalid_data = {
            'system': {'system_name': 'Test System'},
            'measurements': [{'invalid_key': 'invalid_value'}]
        }
        serializer = CombinedSerializer(data=invalid_data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)
