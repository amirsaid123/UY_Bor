from django.urls import path
from apps.views import UserInfoView , UserPropertyListView , VIPPropertyListView


urlpatterns = [
    path('api/v1/user/info/<int:id>/', UserInfoView.as_view(), name='user-info'),
    path('api/v1/user/listings/', UserPropertyListView.as_view(), name='user-property-list'),
    path('api/v1/vip/properties', VIPPropertyListView.as_view(), name='vip-properties'),
]