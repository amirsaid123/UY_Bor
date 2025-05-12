import pytest
from rest_framework import status
from django.urls import reverse
from apps.models import PhoneVerification, User


@pytest.mark.django_db
class TestSendCodeView:
    def test_send_code_view(self, client):
        url = reverse('send_code')
        phone_number = '+998901234567'

        response = client.post(url, data={'phone_number': phone_number}, content_type='application/json')

        assert response.status_code == status.HTTP_201_CREATED
        assert 'phone_number' in response.data
        assert 'random_code' in response.data
        assert response.data['phone_number'] == phone_number
        verification = PhoneVerification.objects.get(phone_number=phone_number)
        assert 100000 <= int(verification.code) <= 999999


@pytest.mark.django_db
class TestUserLoginView:
    @pytest.mark.django_db
    def test_user_login_existing_user(self, client):
        phone_number = "+998901234567"
        code = "123456"

        PhoneVerification.objects.create(phone_number=phone_number, code=code)
        User.objects.create(phone_number=phone_number)

        url = reverse("login")
        payload = {
            "phone_number": phone_number,
            "code": code,
        }

        response = client.post(url, data=payload, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert "tokens" in response.data
        assert "access" in response.data["tokens"]
        assert "refresh" in response.data["tokens"]
        assert response.data["message"] == "User logged in"

    @pytest.mark.django_db
    def test_user_login_creates_user(self, client):
        phone_number = "+998901234568"
        code = "654321"

        PhoneVerification.objects.create(phone_number=phone_number, code=code)

        url = reverse("login")
        payload = {
            "phone_number": phone_number,
            "code": code,
        }

        response = client.post(url, data=payload, content_type="application/json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "User registered and logged in"
        assert User.objects.filter(phone_number=phone_number).exists()

    @pytest.mark.django_db
    def test_user_login_invalid_code(self, client):
        phone_number = "+998901234569"
        PhoneVerification.objects.create(phone_number=phone_number, code="111111")

        url = reverse("login")
        payload = {
            "phone_number": phone_number,
            "code": "999999",
        }

        response = client.post(url, data=payload, content_type="application/json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Invalid code"