import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    status = django_filters.CharFilter(field_name="status", lookup_expr='exact')
    type = django_filters.CharFilter(field_name="type", lookup_expr='exact')
    category = django_filters.CharFilter(field_name="category", lookup_expr='icontains')
    id = django_filters.NumberFilter(field_name="id", lookup_expr='exact')

    class Meta:
        model = Property
        fields = ['status', 'type', 'category', 'id', 'min_price', 'max_price']
