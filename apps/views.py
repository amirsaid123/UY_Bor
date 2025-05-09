import random
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .filters import PropertyFilter, WishlistFilter
from .models import PhoneVerification, User, Wishlist, Property, Tariff, Transaction
from .serializers import PhoneNumberSerializer, UserProfileSerializer, UserUpdateSerializer, UserBalanceSerializer, \
    UserBalanceUpdateSerializer, UserMessageSerializer, UserWishlistSerializer, PropertySerializer, \
    UserTariffSerializer, UserTransactionSerializer, SendMessageSerializer
from .serializers import UserLoginSerializer


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
        Transaction.objects.create(user=user, amount=serializer.validated_data['amount'])
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
        return self.get_object().messages.all()


@extend_schema(
    tags=["User"],
    parameters=[
        OpenApiParameter(
            name="min_price",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            description="Minimum price of the property",
        ),
        OpenApiParameter(
            name="max_price",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            description="Maximum price of the property",
        ),
        OpenApiParameter(
            name="status",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Status of the property (exact match)",
        ),
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Type of the property (exact match)",
        ),
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of the property (case-insensitive contains)",
        ),
        OpenApiParameter(
            name="id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="ID of the property (exact match)",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Sort results by: highest_price, lowest_price, less_viewed, popular, newest, oldest",
            enum=["highest_price", "lowest_price", "less_viewed", "popular", "newest", "oldest"],
        ),
    ],
)
class UserPropertyView(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.filter(user=self.request.user)
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            if ordering == 'highest_price':
                queryset = queryset.order_by('-price')
            elif ordering == 'lowest_price':
                queryset = queryset.order_by('price')
            elif ordering == 'less_viewed':
                queryset = queryset.order_by('views')
            elif ordering == 'popular':
                queryset = queryset.order_by('-views')
            elif ordering == 'newest':
                queryset = queryset.order_by('-created_at')
            elif ordering == 'oldest':
                queryset = queryset.order_by('created_at')
        return queryset


@extend_schema(
    tags=["User"],
    parameters=[
        OpenApiParameter(
            name="min_price",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            description="Minimum price of the property",
        ),
        OpenApiParameter(
            name="max_price",
            type=OpenApiTypes.FLOAT,
            location=OpenApiParameter.QUERY,
            description="Maximum price of the property",
        ),
        OpenApiParameter(
            name="type",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Type of the property (exact match)",
        ),
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of the property (case-insensitive contains)",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Sort results by: highest_price, lowest_price, less_viewed, popular, newest, oldest",
            enum=["highest_price", "lowest_price", "less_viewed", "popular", "newest", "oldest"],
        ),
    ],
)
class UserWishlistView(ListAPIView):
    serializer_class = UserWishlistSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WishlistFilter
    ordering_fields = ['property__price', 'property__view_count', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Wishlist.objects.filter(user=self.request.user)
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            if ordering == 'highest_price':
                queryset = queryset.order_by('-property__price')
            elif ordering == 'lowest_price':
                queryset = queryset.order_by('property__price')
            elif ordering == 'less_viewed':
                queryset = queryset.order_by('property__view_count')
            elif ordering == 'popular':
                queryset = queryset.order_by('-property__view_count')
            elif ordering == 'newest':
                queryset = queryset.order_by('-created_at')
            elif ordering == 'oldest':
                queryset = queryset.order_by('created_at')
        return queryset


@extend_schema(tags=["User"])
class UserTariffView(ListAPIView):
    serializer_class = UserTariffSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.get_object().tariffs.all()


@extend_schema(tags=["User"])
class UserTransactionView(ListAPIView):
    serializer_class = UserTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        return self.get_object().transactions.all()


@extend_schema(tags=["User"])
class UserSendMesageView(CreateAPIView):
    serializer_class = SendMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        user.messages.create(
            sender=user,
            receiver=serializer.validated_data['to_user'],
            message=serializer.validated_data['message']
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
