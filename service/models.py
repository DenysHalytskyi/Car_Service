from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Imię")
    last_name = models.CharField(max_length=50, verbose_name="Nazwisko")
    phone_number = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.TextField(blank=True, null=True, verbose_name="Adres")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"


class Vehicle(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="vehicles", verbose_name="Właściciel")
    brand = models.CharField(max_length=50, verbose_name="Marka")
    model = models.CharField(max_length=50, verbose_name="Model")
    registration_number = models.CharField(max_length=15, unique=True, verbose_name="Numer rejestracyjny")
    vin = models.CharField(max_length=17, unique=True, verbose_name="Numer VIN")
    manufacture_year = models.PositiveIntegerField(verbose_name="Rok produkcji")
    mileage = models.PositiveIntegerField(verbose_name="Przebieg (km)")

    def __str__(self):
        return f"{self.brand} {self.model} ({self.registration_number})"

    class Meta:
        verbose_name = "Pojazd"
        verbose_name_plural = "Pojazdy"


class Part(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa części")
    manufacturer_code = models.CharField(max_length=50, unique=True, verbose_name="Kod producenta")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena jednostkowa (PLN)")
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Ilość w magazynie")

    def __str__(self):
        return f"{self.name} ({self.manufacturer_code})"

    class Meta:
        verbose_name = "Część"
        verbose_name_plural = "Części"


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nazwa usługi")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Cena usługi (PLN)")

    def __str__(self):
        return f"{self.name} - {self.price} PLN"

    class Meta:
        verbose_name = "Usługa"
        verbose_name_plural = "Usługi"


class ServiceOrder(models.Model):
    class OrderStatus(models.TextChoices):
        ACCEPTED = 'ACCEPTED', 'Przyjęte'
        IN_PROGRESS = 'IN_PROGRESS', 'W trakcie naprawy'
        WAITING_FOR_PARTS = 'WAITING_FOR_PARTS', 'Oczekuje na części'
        COMPLETED = 'COMPLETED', 'Zakończone'
        CANCELLED = 'CANCELLED', 'Anulowane'

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="orders", verbose_name="Pojazd")
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders", verbose_name="Pracownik")
    issue_description = models.TextField(verbose_name="Opis usterki")
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.ACCEPTED, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data przyjęcia")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Data zakończenia")
    services = models.ManyToManyField(Service, blank=True, verbose_name="Wykonane usługi")

    def __str__(self):
        return f"Zlecenie #{self.id} | {self.vehicle.registration_number} | {self.get_status_display()}"

    class Meta:
        verbose_name = "Zlecenie serwisowe"
        verbose_name_plural = "Zlecenia serwisowe"


class UsedPart(models.Model):
    order = models.ForeignKey(ServiceOrder, on_delete=models.CASCADE, related_name="used_parts")
    part = models.ForeignKey(Part, on_delete=models.PROTECT, verbose_name="Część")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Ilość")

    def __str__(self):
        return f"{self.quantity}x {self.part.name} -> Zlecenie #{self.order.id}"

    class Meta:
        verbose_name = "Wykorzystana część"
        verbose_name_plural = "Wykorzystane części"
