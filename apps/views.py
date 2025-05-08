from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Blog
from apps.serializers import BlogSerializer, UserBalanceSerializer, TariffSerializer


@extend_schema(tags=['Cid'])
class BlogListApiView(ListAPIView):
    queryset = Blog.objects.all().order_by('-id')
    serializer_class = BlogSerializer

@extend_schema(tags=['Cid'])
class UserBalanceApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserBalanceSerializer(request.user)
        return Response([serializer.data])

@extend_schema(tags=['Cid'])
class UserTariffApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = TariffSerializer(request.user)
        return Response(serializer.data)
