from rest_framework.serializers import ModelSerializer
from .models import HydroponicSystem


class HydroponicSystemSerializer(ModelSerializer):
    class Meta:
        model = HydroponicSystem
        fields = (
            "system_name",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_field = ["created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user

        system = HydroponicSystem.objects.create(owner=user, **validated_data)
        return system
