from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

class UserBalanceApiTest(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            phone_number='+9981234568',
            password='test1234',
            first_name='Cid',
            last_name='Kagenou',
            balance=17.99
        )

        self.client.force_authenticate(user=self.user)

    def test_user_balance_response(self):
        url = reverse('user-balance')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['first_name'], 'Cid')
        self.assertEqual(response.data[0]['last_name'], 'Kagenou')
        self.assertEqual(response.data[0]['phone_number'], '+9981234568')
        self.assertEqual(float(response.data[0]['balance']), 17.99)

