from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from apps.models import User, Transaction, Category, City, Region, ResidentialComplex, Property
from django.test import TestCase


class FillBalanceViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(card_number='1234567890123456', balance=10000.00)
        self.url = reverse('fill-balance')

    def test_fill_balance_success(self):
        data = {
            "card_number": "1234567890123456",
            "amount": 5000.00
        }
        response = self.client.post(self.url, data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertEqual(response.data['message'], "Balans muvaffaqiyatli to‘ldirildi")

        self.user.refresh_from_db()
        self.assertEqual(self.user.balance, 15000)

    def test_fill_balance_card_not_found(self):
        data = {
            "card_number": "0000000000000000",
            "amount": 3000
        }
        response = self.client.post(self.url, data, format='json')
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertIn("Karta raqami topilmadi", response.data['error'])


class TransactionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(phone_number='+998901234567', email='user@example.com')
        self.transaction1 = Transaction.objects.create(user=self.user, amount=150.00)

    def test_transaction_list(self):
        url = reverse('user_transactions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['amount'], '150.00')
        self.assertEqual(response.data[0]['user'], self.user.id)


# class ResidentialComplexListAPIViewTest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#
#         self.user = User.objects.create_user(phone_number="1234567890", password="123")
#         self.category = Category.objects.create(name="nimadir")
#         self.city = City.objects.create(name="new york", region=None)
#         self.region = Region.objects.create(name="nimadir", country=None)
#         self.res_complex = ResidentialComplex.objects.create(name="qandaydir joy", description="hrtg erghub jrnefndhj")
#         self.property = Property.objects.create(
#             name="Spacious 2BHK",
#             address="123 Park Ave",
#             building_material="brick",
#             renovation_needed="euro",
#             area=120.5,
#             room=2,
#             floor=5,
#             price=200000,
#             description="A beautiful 2BHK apartment",
#             type="sale",
#             category=self.category,
#             residential_complex=self.res_complex,
#             city=self.city,
#             region=self.region,
#             user=self.user,
#         )
#
#     def test_residential_complex_list_view(self):
#         response = self.client.get('residential-complex')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data[0]['name'], "Luxury Living")
