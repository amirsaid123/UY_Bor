from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import *


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'organization', 'role', 'phone_number']
        extra_kwargs = {
            'phone_number': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'organization': {'required': False},
            'role': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.organization = validated_data.get('organization', instance.organization)
        instance.role = validated_data.get('role', instance.role)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance


class UserShortSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'phone_number']


class PropertyShortSerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'


class WishlistSerializer(ModelSerializer):
    user = UserShortSerializer()
    property = PropertyShortSerializer()

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'property']

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ['id', 'title', 'slug', 'description', 'image', 'created_at']