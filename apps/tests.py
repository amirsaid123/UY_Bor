from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from apps.models import User, Transaction


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
        url = reverse('user-transactions')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['amount'], '150.00')
        self.assertEqual(response.data[0]['user'], self.user.id)
