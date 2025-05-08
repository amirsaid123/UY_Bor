from django.urls import path
from apps.views import BlogListApiView, UserBalanceApiView, UserTariffApiView

# Cid
urlpatterns = [
    path('blog/', BlogListApiView.as_view(), name='blog-list'),
    path('balance/', UserBalanceApiView.as_view(), name='user-balance'),
    path('tariff/', UserTariffApiView.as_view(), name='user-tariff'),
]
