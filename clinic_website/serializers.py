from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    """Сериализатор записи на прием к врачу."""

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("status", "patient", "created_at")
