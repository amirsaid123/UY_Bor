import django_filters
from .models import Property, Wishlist


class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    status = django_filters.CharFilter(field_name="status", lookup_expr='exact')
    type = django_filters.CharFilter(field_name="type", lookup_expr='exact')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name="id", lookup_expr='exact')

    class Meta:
        model = Property
        fields = ['status', 'type', 'category', 'id', 'min_price', 'max_price']


class WishlistFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="property__price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="property__price", lookup_expr='lte')
    type = django_filters.CharFilter(field_name="property__type", lookup_expr='exact')
    category = django_filters.CharFilter(field_name="property__category__name", lookup_expr='icontains')

    class Meta:
        model = Wishlist
        fields = ['type', 'category', 'min_price', 'max_price']

class SearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(field_name="address", lookup_expr='icontains')
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    type = django_filters.CharFilter(field_name="type", lookup_expr='exact')
    category = django_filters.CharFilter(field_name="category__name", lookup_expr='exact')
    renovation_needed = django_filters.CharFilter(field_name="renovation_needed", lookup_expr='exact')
    label = django_filters.CharFilter(field_name="label", lookup_expr='exact')
    residential_type = django_filters.CharFilter(field_name="residential_type", lookup_expr='exact')
    material = django_filters.CharFilter(field_name="building_material", lookup_expr='icontains')

    room = django_filters.NumberFilter(field_name="room", lookup_expr='exact')
    floor = django_filters.NumberFilter(field_name="floor", lookup_expr='exact')
    repair = django_filters.CharFilter(field_name="repair", lookup_expr='exact')
    commissioning_date = django_filters.DateFilter(field_name="commissioning_date", lookup_expr='exact')
    min_area = django_filters.NumberFilter(field_name="area", lookup_expr='gte')
    max_area = django_filters.NumberFilter(field_name="area", lookup_expr='lte')
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')

    residential_name = django_filters.CharFilter(field_name="residential_complex__name", lookup_expr='icontains')
    city = django_filters.CharFilter(field_name="city__name", lookup_expr='icontains')
    region = django_filters.CharFilter(field_name="region__name", lookup_expr='icontains')
    metro = django_filters.CharFilter(field_name="metro__name", lookup_expr='icontains')
    district = django_filters.CharFilter(field_name="district__name", lookup_expr='icontains')
    country = django_filters.CharFilter(field_name="country__name", lookup_expr='icontains')

    created_after = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Property
        fields = [
            'search', 'name', 'type', 'category', 'renovation_needed', 'label',
            'residential_type', 'material', 'room', 'floor', 'repair',
            'commissioning_date', 'min_area', 'max_area', 'min_price', 'max_price',
            'residential_name', 'city', 'region', 'metro', 'district', 'country',
            'created_after', 'created_before'
        ]