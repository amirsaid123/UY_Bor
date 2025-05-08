from rest_framework import serializers
from .models import User , Property

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'organization', 'phone_number']



class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'