from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Part, ServiceOrder, Vehicle, Customer


class InventoryTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testadmin', password='testpassword')
        response = self.client.post('/api/token/', {'username': 'testadmin', 'password': 'testpassword'})
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.part = Part.objects.create(
            name="Klocki hamulcowe",
            manufacturer_code="BR-01",
            price="100.00",
            stock_quantity=10
        )
        self.customer = Customer.objects.create(
            first_name="Jan", last_name="Kowalski", phone_number="+48123456789"
        )
        self.vehicle = Vehicle.objects.create(
            customer=self.customer, brand="Audi", model="A4",
            registration_number="WA123", vin="12345678901234567",
            manufacture_year=2015, mileage=200000
        )
        self.order = ServiceOrder.objects.create(
            vehicle=self.vehicle, issue_description="Wymiana klocków", status="ACCEPTED"
        )

    def test_stock_reduction_on_used_part_creation(self):

        url = '/api/used-parts/'
        data = {
            "order": self.order.id,
            "part": self.part.id,
            "quantity": 2
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.part.refresh_from_db()

        self.assertEqual(self.part.stock_quantity, 8)

    def test_unauthorized_access(self):
        self.client.credentials()

        response = self.client.get('/api/customers/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
