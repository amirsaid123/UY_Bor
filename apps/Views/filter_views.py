from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.Serializers.filter_serializers import PropertySerializer, MessageSerializer
from apps.filters import SearchPropertyFilter
from apps.models import Property, Message


@extend_schema(
    tags=["Search"],
    parameters=[
        OpenApiParameter(name="search", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Search by address (case-insensitive)"),
        OpenApiParameter(name="name", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Search by property name (case-insensitive)"),
        OpenApiParameter(name="description", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Search by description (case-insensitive)"),
        OpenApiParameter(name="type", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Property type (e.g., 'sale', 'rent')",
                         enum=[c[0] for c in Property.Type.choices]),
        OpenApiParameter(name="category", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Category name (case-insensitive contains)"),
        OpenApiParameter(name="building_material", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Building material (e.g., 'brick')",
                         enum=[c[0] for c in Property.Material.choices]),
        OpenApiParameter(name="renovation_needed", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Renovation status (e.g., 'euro')",
                         enum=[c[0] for c in Property.Renovation.choices]),
        OpenApiParameter(name="repair", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Repair status (e.g., 'author')", enum=[c[0] for c in Property.Repair.choices]),
        OpenApiParameter(name="label", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Label (e.g., 'vip')", enum=[c[0] for c in Property.Label.choices]),
        OpenApiParameter(name="residential_type", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Residential type (e.g., 'free_layout')",
                         enum=[c[0] for c in Property.ResidentialType.choices]),
        OpenApiParameter(name="status", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Property status (e.g., 'active')", enum=[c[0] for c in Property.Status.choices]),
        OpenApiParameter(name="room", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Number of rooms (exact)"),
        OpenApiParameter(name="floor", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Floor number (exact)"),
        OpenApiParameter(name="min_area", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Minimum area (sqm)"),
        OpenApiParameter(name="max_area", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Maximum area (sqm)"),
        OpenApiParameter(name="min_price", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Minimum price"),
        OpenApiParameter(name="max_price", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Maximum price"),
        OpenApiParameter(name="min_views", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Minimum view count"),
        OpenApiParameter(name="max_views", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Maximum view count"),
        OpenApiParameter(name="min_saves", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Minimum save count"),
        OpenApiParameter(name="max_saves", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Maximum save count"),
        OpenApiParameter(name="residential_name", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Residential complex name (case-insensitive)"),
        OpenApiParameter(name="city", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="City name (case-insensitive)"),
        OpenApiParameter(name="region", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Region name (case-insensitive)"),
        OpenApiParameter(name="metro", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Metro station name (case-insensitive)"),
        OpenApiParameter(name="district", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="District name (case-insensitive)"),
        OpenApiParameter(name="country", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Country name (case-insensitive)"),
        OpenApiParameter(name="amenities", type={"type": "array", "items": {"type": "string"}},
                         location=OpenApiParameter.QUERY, description="List of amenity names (e.g., ['pool', 'gym'])"),
        OpenApiParameter(name="commissioning_date", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY,
                         description="Exact commissioning date"),
        OpenApiParameter(name="min_commissioning_date", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY,
                         description="Minimum commissioning date"),
        OpenApiParameter(name="max_commissioning_date", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY,
                         description="Maximum commissioning date"),
        OpenApiParameter(name="created_after", type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                         description="Created after date"),
        OpenApiParameter(name="created_before", type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                         description="Created before date"),
        OpenApiParameter(name="updated_after", type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                         description="Updated after date"),
        OpenApiParameter(name="updated_before", type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                         description="Updated before date"),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Sort results by: highest_price, lowest_price, less_viewed, popular, newest, oldest",
            enum=["highest_price", "lowest_price", "less_viewed", "popular", "newest", "oldest"],
        ),
    ],
)
class SearchProperty(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = SearchPropertyFilter
    ordering_fields = ['price', 'views', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.all()
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
    tags=["Property"],
)
class PropertyView(RetrieveAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]
    lookup_field = 'id'

    def get_object(self):
        return Property.objects.get(id=self.kwargs['pk'])


@extend_schema(
    tags=["UserMessages"],
)
class UserMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
