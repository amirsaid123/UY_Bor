import re
from rest_framework import serializers
from apps.models import User


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        pattern = r'^\+998\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid Uzbek phone number starting with +998.")
        return value


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    code = serializers.CharField()

    def validate_phone_number(self, value):
        pattern = r'^\+998\d{9}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid Uzbek phone number starting with +998.")
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'email', 'avatar', 'role']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']

class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'balance']




class UserBalanceUpdateSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    password = serializers.CharField(max_length=4)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_card_number(self, value):
        pattern = r'^\d{16}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid 16-digit card number.")
        return value

    def validate_password(self, value):
        pattern = r'^\d{4}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Enter a valid 4-digit password.")
        return value
