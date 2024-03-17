from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import HydroponicSystem, Measurements
from .serializers import CombinedSerializer, MeasurementsSerializer, SystemMeasurementsSerializer
from rest_framework.exceptions import PermissionDenied, NotFound


class HydroponicSystemMeasurementsListCreate(generics.ListAPIView):
    queryset = HydroponicSystem.objects.all()
    serializer_class = SystemMeasurementsSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        user = self.request.user
        hydroponic_system = get_object_or_404(HydroponicSystem,
                                              id=system_id, owner=user)
        return HydroponicSystem.objects.filter(id=hydroponic_system.id)


class Last10MeasurementsList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CombinedSerializer

    def get_queryset(self):
        system_id = self.kwargs.get('system_id')
        if not HydroponicSystem.objects.filter(id=system_id).exists():
            raise NotFound("Hydroponic system with the specified ID does not exist.") # noqa
        user = self.request.user
        if not HydroponicSystem.objects.filter(
                id=system_id, owner=user).exists():
            raise PermissionDenied(
                "You do not have permission to access this hydroponic system.")
        return Measurements.objects.filter(
            hydroponic_system_id=system_id).order_by('-date')[:10]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        system_id = self.kwargs.get('system_id')
        hydroponic_system = HydroponicSystem.objects.get(id=system_id)
        serializer = CombinedSerializer(
            {'system': hydroponic_system,
             'measurements': queryset})
        return Response(serializer.data)


class AddMeasurement(generics.CreateAPIView):
    serializer_class = MeasurementsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        system_id = self.kwargs.get('system_id')
        user = self.request.user
        hydroponic_system = get_object_or_404(HydroponicSystem,
                                              id=system_id, owner=user)
        serializer.save(hydroponic_system=hydroponic_system)
