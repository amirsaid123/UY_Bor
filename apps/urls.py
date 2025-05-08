from django.urls import path
from apps.views import UserInfoView , UserPropertyListView


urlpatterns = [
    path('api/v1/user/info/<int:id>/', UserInfoView.as_view(), name='user-info'),
    path('api/v1/user/listings/', UserPropertyListView.as_view(), name='user-property-list'),
]