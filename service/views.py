from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F
from .models import Customer, Vehicle, Part, Service, ServiceOrder, UsedPart
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    CustomerSerializer, VehicleSerializer, PartSerializer,
    ServiceSerializer, ServiceOrderSerializer, UsedPartSerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['last_name', 'phone_number']


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

    @action(detail=True, methods=['get'], url_path='total-cost')
    def calculate_total_cost(self, request, pk=None):
        #Total
        order = self.get_object()
        #All services
        services_cost = order.services.aggregate(total=Sum('price'))['total'] or 0
        #Spare parts used
        parts_cost = order.used_parts.aggregate(total=Sum(F('quantity') * F('part__price')))['total'] or 0

        total_cost = services_cost + parts_cost

        return Response({
            'order_id': order.id,
            'services_cost': services_cost,
            'parts_cost': parts_cost,
            'total_cost': total_cost
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')

        if new_status not in ServiceOrder.OrderStatus.values:
            return Response({'error': 'Invalid status choice.'},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        order.status = new_status
        order.save()
        return Response({'status': f'Order status updated to {order.status}'})


class UsedPartViewSet(viewsets.ModelViewSet):
    queryset = UsedPart.objects.all()
    serializer_class = UsedPartSerializer
