from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


@extend_schema(tags=['User'])
class UserUpdateView(UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user


@extend_schema(tags=['User'])
class UserWishlistView(APIView):
    serializer_class = WishlistSerializer
    def get(self, request, user_id):
        wishlist_items = Wishlist.objects.filter(user_id=user_id)
        serializer = WishlistSerializer(wishlist_items, many=True)
        return Response(serializer.data)



@extend_schema(tags=['Blog'])
class BlogListView(generics.ListAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
