from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .serializers import UserRegisterSerializer
from .models import User
import random


# Create your views here.


@extend_schema(tags=["user_register"],
               parameters=[
                   OpenApiParameter(
                       name='phone_number',
                       type=str,
                       location=OpenApiParameter.QUERY,
                       required=True,
                       description="Enter a phone number"
                   )
               ])
class UserRegisterView(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.query_params['phone_number']
        random_code = random.randint(10**5, 10**6)

        serializer = UserRegisterSerializer(data={"phone_number": phone_number})
        if serializer.is_valid():
            serializer.save()
            return Response({
                'phone_number': phone_number,
                'random_code': random_code
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)