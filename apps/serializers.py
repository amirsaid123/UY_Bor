from rest_framework import serializers

from apps.models import Transaction


class BalanceFillSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'