from django.contrib import admin
from .models import Customer, Vehicle, Part, Service, ServiceOrder, UsedPart


admin.site.register(Customer)
admin.site.register(Vehicle)
admin.site.register(Part)
admin.site.register(Service)
admin.site.register(ServiceOrder)
admin.site.register(UsedPart)
