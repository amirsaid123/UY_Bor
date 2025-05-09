from rest_framework import serializers

from apps.models import Property, Image, Amenity


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class PropertySerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = '__all__'
