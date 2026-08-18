from rest_framework import serializers
from .models import Customer, Vehicle, Part, Service, ServiceOrder, UsedPart

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class UsedPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsedPart
        fields = '__all__'


class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'
