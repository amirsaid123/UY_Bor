from rest_framework import serializers

from apps.models import Property


class SearchFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'