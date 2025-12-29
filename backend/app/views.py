from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import City
from .serializers import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.all()
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return City.objects.filter(is_active=True).order_by("id")

    def destroy(self, request, *args, **kwargs):
        city = self.get_object()
        city.is_active = False
        city.save(update_fields=["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)
