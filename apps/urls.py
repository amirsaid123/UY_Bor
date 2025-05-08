from django.urls import path

from apps.views import FillBalanceView, TransactionListApiView

#asqar
urlpatterns = [
    path('user/fill/balance/', FillBalanceView.as_view(), name='fill-balance'),
    path('user/transactions/', TransactionListApiView.as_view(), name='user-transactions')
]