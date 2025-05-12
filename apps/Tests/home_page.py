import pytest
from django.urls import reverse
from rest_framework import status
from apps.models import (Property, Category, City, Metro, District, Country, Amenity,
                         User, Region)

@pytest.mark.django_db
class TestHomePageView:
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
            label="vip",
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

    def test_home_page_view(self, client, property):
        url = reverse('vip_property')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
        print(response.data)

    def test_residential_complex(self, client, property):
        url = reverse('residential_complex')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_videos_view(self, client):
        url = reverse('videos')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_blogs_view(self, client):
        url = reverse('blogs')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK

    def test_static_pages_view(self, client):
        url = reverse('static_pages')
        response = client.get(url, content_type='application/json')
        assert response.status_code == status.HTTP_200_OK
