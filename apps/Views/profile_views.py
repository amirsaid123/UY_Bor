from decimal import Decimal
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from apps.Serializers import UserProfileSerializer, UserUpdateSerializer, UserBalanceSerializer, \
    UserBalanceUpdateSerializer, UserMessageSerializer, UserWishlistSerializer, PropertySerializer, \
    UserTariffSerializer, UserTransactionSerializer, SendMessageSerializer, DeactivatePropertySerializer, \
    UserUpdateWishlistSerializer, DeletePropertySerializer
from apps.filters import PropertyFilter, WishlistFilter
from apps.models import Wishlist, Property, Transaction


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

        user.balance = Decimal(user.balance) + serializer.validated_data['amount']
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


@extend_schema(tags=["User"])
class UserDeactivatePropertyView(UpdateAPIView):
    serializer_class = DeactivatePropertySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.properties.get(pk=self.kwargs['pk'])
        except Property.DoesNotExist:
            raise Http404("Property not found or does not belong to the user")

    def update(self, request, *args, **kwargs):
        property_obj = self.get_object()
        if property_obj.status == Property.Status.INACTIVE:
            return Response(
                {"detail": "Property is already inactive"},
                status=HTTP_400_BAD_REQUEST
            )
        property_obj.status = Property.Status.INACTIVE
        property_obj.save()
        serializer = PropertySerializer(property_obj)
        return Response(serializer.data, status=HTTP_200_OK)


@extend_schema(tags=["User"])
class UserUpdateWishlistView(UpdateAPIView):
    serializer_class = UserUpdateWishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Property.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        property_obj = self.get_object()
        user = request.user

        wishlist_entry, created = Wishlist.objects.get_or_create(user=user, property=property_obj)

        if not created:
            wishlist_entry.delete()
            return Response({"detail": "Removed from wishlist."}, status=HTTP_200_OK)

        return Response({"detail": "Added to wishlist."}, status=HTTP_201_CREATED)


@extend_schema(tags=["User"])
class UserDeletePropertyView(DestroyAPIView):
    serializer_class = DeletePropertySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.properties.get(pk=self.kwargs['pk'])


    def delete(self, request, *args, **kwargs):
        property_obj = self.get_object()
        property_obj.delete()
        return Response({"detail": "Property deleted successfully."}, status=HTTP_200_OK)



