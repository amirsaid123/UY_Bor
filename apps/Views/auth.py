import random
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.Serializers import PhoneNumberSerializer, UserLoginSerializer
from apps.models import PhoneVerification, User


@extend_schema(tags=["Authentication"])
class SendCodeView(CreateAPIView):
    serializer_class = PhoneNumberSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']
        random_code = random.randint(100000, 999999)

        PhoneVerification.objects.update_or_create(
            phone_number=phone_number,
            defaults={'code': random_code}
        )

        return Response({
            'phone_number': phone_number,
            'random_code': random_code
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Authentication"])
class UserLoginView(GenericAPIView):
    serializer_class = UserLoginSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def validate_code(self, phone_number, code):
        verification = PhoneVerification.objects.filter(phone_number=phone_number).first()
        if not verification:
            return False
        if verification.code != code:
            return False
        verification.delete()
        return True

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        code = request.data.get('code')

        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST)

        is_valid_phone_number = PhoneVerification.objects.filter(phone_number=phone_number).exists()
        if not is_valid_phone_number:
            return Response({"detail": "Invalid Phone Number"}, status=status.HTTP_400_BAD_REQUEST)

        is_valid_code = self.validate_code(phone_number, code)
        if not is_valid_code:
            return Response({"detail": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(phone_number=phone_number)

        tokens = self.get_tokens_for_user(user)

        return Response({
            "message": "User logged in" if not created else "User registered and logged in",
            "user_id": user.id,
            "phone_number": user.phone_number,
            "tokens": tokens
        }, status=status.HTTP_200_OK)
