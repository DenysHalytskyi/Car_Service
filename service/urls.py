from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CustomerViewSet, VehicleViewSet, PartViewSet,
    ServiceViewSet, ServiceOrderViewSet, UsedPartViewSet
)


router = DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'parts', PartViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'orders', ServiceOrderViewSet)
router.register(r'used-parts', UsedPartViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
