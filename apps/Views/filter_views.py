from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.Serializers.filter_serializers import SearchFilterSerializer
from apps.filters import SearchFilter
from apps.models import Property


@extend_schema(
    tags=["Search"],
    parameters=[
        OpenApiParameter(name="search", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Search by address"),
        OpenApiParameter(name="name", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Search by property name"),
        OpenApiParameter(name="type", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Type of property"),
        OpenApiParameter(name="category", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Category name"),
        OpenApiParameter(name="renovation_needed", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Is renovation needed? (true/false)"),
        OpenApiParameter(name="label", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Label of the property"),
        OpenApiParameter(name="residential_type", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Residential type of the property"),
        OpenApiParameter(name="material", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Building material"),
        OpenApiParameter(name="room", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Number of rooms"),
        OpenApiParameter(name="floor", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Floor number"),
        OpenApiParameter(name="repair", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY,
                         description="Repair status/level"),
        OpenApiParameter(name="commissioning_date", type=OpenApiTypes.DATE, location=OpenApiParameter.QUERY,
                         description="Date of commissioning"),
        OpenApiParameter(name="min_area", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Minimum area in m²"),
        OpenApiParameter(name="max_area", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Maximum area in m²"),
        OpenApiParameter(name="min_price", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Minimum price of the property"),
        OpenApiParameter(name="max_price", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY,
                         description="Maximum price of the property"),
        OpenApiParameter(name="residential_name", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Residential complex name"),
        OpenApiParameter(name="city", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY, description="City name"),
        OpenApiParameter(name="region", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Region name"),
        OpenApiParameter(name="metro", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Metro station name"),
        OpenApiParameter(name="district", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="District name"),
        OpenApiParameter(name="country", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Country name"),
        OpenApiParameter(name="created_after", type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                         description="Filter properties created after this datetime"),
        OpenApiParameter(name="created_before", type=OpenApiTypes.DATETIME, location=OpenApiParameter.QUERY,
                         description="Filter properties created before this datetime"),
        OpenApiParameter(name="ordering", type=OpenApiTypes.STR, location=OpenApiParameter.QUERY,
                         description="Sort results by: highest_price, lowest_price, less_viewed, popular, newest, oldest",
                         enum=["highest_price", "lowest_price", "less_viewed", "popular", "newest", "oldest"],
                         ),
    ]
)
class SearchProperty(ListAPIView):
    serializer_class = SearchFilterSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SearchFilter
    ordering_fields = ['property__price', 'property__view_count', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Property.objects.all()
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
