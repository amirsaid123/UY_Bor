import re

from rest_framework import serializers

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