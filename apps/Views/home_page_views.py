from rest_framework.generics import ListAPIView

from apps.Serializers.filter_serializers import PropertySerializer
from apps.models import Property


class ResidentialComplexListAPIView(ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        return Property.objects.filter(residential_complex__isnull=False)
