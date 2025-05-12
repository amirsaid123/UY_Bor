import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from apps.models import (Property, Category, City, Metro, District, Country, Amenity,
                         User, Message, Wishlist, Region, Transaction, Tariff)


@pytest.mark.django_db
class TestUserProfileView:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            phone_number="+998901234567", password="testpass123", first_name="Amirsaid", last_name="Samigjanov",
            balance=100.00
        )

    @pytest.fixture
    def property(self, user):
        category = Category.objects.create(name="Apartment")
        country = Country.objects.create(name="Uzbekistan")
        region = Region.objects.create(name="Chilonzor", country=country)
        city = City.objects.create(name="Tashkent", region=region)
        metro = Metro.objects.create(name="Chilonzor")
        district = District.objects.create(name="Yunusabad", city=city)

        amenity = Amenity.objects.create(name="Parking")

        prop = Property.objects.create(
            name="Modern Apartment in Chilonzor",
            address="123 Chilonzor Street",
            building_material="brick",
            renovation_needed="euro",
            area=85.50,
            room=3,
            floor=5,
            price=85000,
            description="A spacious and modern apartment located in the heart of Chilonzor.",
            type="sale",
            category=category,
            label="premium",
            commissioning_date="2025-05-08",
            views=120,
            saves=15,
            city=city,
            metro=metro,
            district=district,
            country=country,
            latitude="41.299500",
            longitude="69.240100",
            status="active",
            user=user,
            region=region,
        )
        prop.amenities.set([amenity])
        return prop

    @pytest.fixture
    def message(self, user):
        return Message.objects.create(receiver=user, message="Hello, this is a test message", sender=user)

    @pytest.fixture
    def wishlist(self, user, property):
        return Wishlist.objects.create(user=user, property=property)

    @pytest.fixture
    def transaction(self, user):
        return Transaction.objects.create(user=user, amount=100.00)

    @pytest.fixture
    def tariff(self, user):
        return Tariff.objects.create(
            name="Basic",
            price="10000.00",
            duration_days=7,
            description="Basic listing for 7 days",
            status="active",
            label="standard",
            created_at="2025-05-09T08:56:01.493Z",
            user=user
        )

    @pytest.fixture
    def auth_client(self, user):
        client = APIClient()
        client.force_authenticate(user=user)
        return client

    def test_user_profile_view(self, auth_client):
        url = reverse('user_profile')
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_user_update_view(self, auth_client, user):
        url = reverse('user_profile_update')
        payload = {
            "first_name": "Test",
            "last_name": "User",
            "password": "testpass123",
        }
        print(user.first_name)
        response = auth_client.patch(url, data=payload, content_type='application/json')
        print(response.data['first_name'])
        assert response.status_code == status.HTTP_200_OK

    def test_user_balance_view(self, auth_client):
        url = reverse('user_balance')
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data['balance'])

    def test_user_balance_update_view(self, auth_client, user):
        url = reverse('user_balance_update')
        payload = {
            "amount": "50.00",
            "card_number": 8600123443126578,
            "password": 1234
        }
        response = auth_client.put(url, data=payload, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data['new_balance'])

    def test_user_messages_view(self, auth_client, message):
        url = reverse('user_messages')
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_user_wishlist_view(self, auth_client, wishlist):
        url = reverse('user_wishlist')
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_user_transactions(self, auth_client, transaction):
        url = reverse('user_transactions')
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_user_tariff_view(self, auth_client, tariff):
        url = reverse('user_tariff')
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_user_send_message(self, auth_client, user):
        url = reverse('user_send_message')
        payload = {
            "to_user": 1,
            "message": "Hello, World! This is a test message from Amirsaid to Amirsaid.",
        }
        response = auth_client.post(url, data=payload, content_type='application/json')
        assert response.status_code == status.HTTP_201_CREATED
        print(response.data)

    def test_user_deactivate_property(self, auth_client, property):
        url = reverse('deactivate_property', kwargs={'pk': property.id})
        response = auth_client.patch(url, content_type='application/json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'inactive'

    def test_user_property_view(self, auth_client, property):
        url = reverse('user_listings') + "?status=active"
        response = auth_client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_user_wishlist_update(self, auth_client, wishlist, property):
        url = reverse('user_wishlist_update', kwargs={'pk': property.id})
        response = auth_client.patch(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_user_property_delete(self, auth_client, property):
        url = reverse('user_property_delete', kwargs={'pk': property.id})
        response = auth_client.delete(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)