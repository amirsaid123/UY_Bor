import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    price_from = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_to = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    area_from = django_filters.NumberFilter(field_name='area', lookup_expr='gte')
    area_to = django_filters.NumberFilter(field_name='area', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='iexact')
    region = django_filters.CharFilter(field_name='region__slug', lookup_expr='iexact')
    city = django_filters.CharFilter(field_name='city__slug', lookup_expr='iexact')
    district = django_filters.CharFilter(field_name='district__slug', lookup_expr='iexact')
    metro = django_filters.CharFilter(field_name='metro__slug', lookup_expr='iexact')

    class Meta:
        model = Property
        fields = [
            'type', 'status', 'label', 'building_material', 'renovation_needed',
            'room', 'floor', 'residential_type',
        ]