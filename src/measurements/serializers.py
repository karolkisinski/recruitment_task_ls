from rest_framework import serializers

from hydroponic_system.models import HydroponicSystem
from hydroponic_system.serializers import HydroponicSystemSerializer
from .models import Measurements


class MeasurementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurements
        fields = ['id', 'ph', 'water_temperature', 'tds', 'date']


class SystemMeasurementsSerializer(serializers.ModelSerializer):
    measurements = MeasurementsSerializer(many=True)

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'system_name', 'measurements']


class CombinedSerializer(serializers.Serializer):
    system = HydroponicSystemSerializer()
    measurements = MeasurementsSerializer(many=True)
