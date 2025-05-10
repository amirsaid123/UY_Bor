from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from apps.Serializers import PropertySerializer
from apps.Serializers.home_page_serializers import ResidentialComplexSerializer, VideoSerializer, BlogSerializer, \
    StaticPageSerializer
from apps.models import Property, Video, Blog, StaticPage


@extend_schema(tags=["Home"])
class VipPropertyView(ListAPIView):
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Property.objects.filter(label='vip')


@extend_schema(tags=["Home"])
class ResidentialComplexView(ListAPIView):
    serializer_class = ResidentialComplexSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Property.objects.filter(residential_complex__isnull=False)


@extend_schema(tags=["Home"])
class VideoView(ListAPIView):
    serializer_class = VideoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Video.objects.all()


@extend_schema(tags=["Home"])
class BlogView(ListAPIView):
    serializer_class = BlogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Blog.objects.all()


@extend_schema(tags=["Home"])
class StaticPageView(ListAPIView):
    serializer_class = StaticPageSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return StaticPage.objects.all()
