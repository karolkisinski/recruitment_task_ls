from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import HydroponicSystem
from .serializers import HydroponicSystemSerializer


class HydroponicSystemListCreate(generics.ListCreateAPIView):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return HydroponicSystem.objects.filter(owner=user)


class HydroponicSystemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView): # noqa
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        return HydroponicSystem.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            raise PermissionDenied(
                "You do not have permission to access this system.")
        return obj

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())
