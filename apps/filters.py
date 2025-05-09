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
