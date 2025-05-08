from decimal import Decimal

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import User, Transaction
from apps.serializers import TransactionSerializer


@extend_schema(tags=['asqar'])
class FillBalanceView(APIView):
    def post(self, request):
        card_number = request.data.get("card_number")
        amount = Decimal(request.data.get("amount"))

        try:
            user = User.objects.get(card_number=card_number)
        except User.DoesNotExist:
            return Response({"error": "Karta raqami topilmadi"}, status=status.HTTP_400_BAD_REQUEST)

        user.balance += amount

        user.save()
        return Response({"message": "Balans muvaffaqiyatli to‘ldirildi"}, status=status.HTTP_200_OK)


@extend_schema(tags=['asqar'])
class TransactionListApiView(ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer