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

    def validate(self, attrs):
        part = attrs.get('part')
        quantity = attrs.get('quantity', 1)

        if self.instance:
            diff = quantity - self.instance.quantity
            if part.stock_quantity < diff:
                raise serializers.ValidationError(
                    {"quantity": f"Brak wystarczającej ilości w magazynie. Dostępno: {part.stock_quantity}"}
                )
        else:
            if part.stock_quantity < quantity:
                raise serializers.ValidationError(
                    {"quantity": f"Brak wystarczającej ilości w magazynie. Dostępno: {part.stock_quantity}"}
                )

        return attrs


class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = '__all__'
