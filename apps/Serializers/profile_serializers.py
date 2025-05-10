import re

from rest_framework import serializers

from apps.models import User, Message, Property, Tariff, Transaction, Image, Amenity


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


class UserMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class UserWishlistSerializer(serializers.Serializer):
    property = PropertySerializer()


class UserTariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'name', 'price', 'description', 'duration_days', 'status', 'label', 'created_at']


class UserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'created_at']


class SendMessageSerializer(serializers.Serializer):
    to_user = serializers.IntegerField()
    message = serializers.CharField(max_length=1000)


class DeactivatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id']
