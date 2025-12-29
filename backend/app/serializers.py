from rest_framework import serializers
from .models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "country",
            "latitude",
            "longitude",
            "main_tourist_site",
            "population",
            "has_seaport",
            "temperature",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["temperature", "is_active", "created_at", "updated_at"]

    def validate_latitude(self, value: float) -> float:
        if value < -90 or value > 90:
            raise serializers.ValidationError("latitude debe estar entre -90 y 90.")
        return value

    def validate_longitude(self, value: float) -> float:
        if value < -180 or value > 180:
            raise serializers.ValidationError("longitude debe estar entre -180 y 180.")
        return value

    def validate_population(self, value: int) -> int:
        if value <= 0:
            raise serializers.ValidationError("population debe ser mayor a 0.")
        return value
