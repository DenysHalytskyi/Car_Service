from rest_framework import viewsets
from .models import Customer, Vehicle, Part, Service, ServiceOrder, UsedPart
from .serializers import (
    CustomerSerializer, VehicleSerializer, PartSerializer,
    ServiceSerializer, ServiceOrderSerializer, UsedPartSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceOrderViewSet(viewsets.ModelViewSet):
    queryset = ServiceOrder.objects.all()
    serializer_class = ServiceOrderSerializer


class UsedPartViewSet(viewsets.ModelViewSet):
    queryset = UsedPart.objects.all()
    serializer_class = UsedPartSerializer
