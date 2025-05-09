import random
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PhoneVerification, User, Message, Wishlist
from .serializers import PhoneNumberSerializer, UserProfileSerializer, UserUpdateSerializer, UserBalanceSerializer, \
    UserBalanceUpdateSerializer, UserMessageSerializer, UserWishlistSerializer
from .serializers import UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken


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

@extend_schema(tags=["User"])
class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user

@extend_schema(tags=['User'])
class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(tags=['User'])
class UserBalanceView(RetrieveAPIView):
    serializer_class = UserBalanceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(tags=['User'])
class UserBalanceUpdateView(UpdateAPIView):
    serializer_class = UserBalanceUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.get_object()

        user.balance += serializer.validated_data['amount']
        user.save()

        return Response({
            'message': 'Balance updated successfully',
            'new_balance': str(user.balance)
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['User'])
class UserMessageView(ListAPIView):
    serializer_class = UserMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return Message.objects.filter(receiver=self.get_object())

@extend_schema(tags=['User'])
class UserWishlistView(ListAPIView):
    serializer_class = UserWishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.get_object())
