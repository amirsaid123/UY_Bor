from django.urls import path
from apps.Views import SendCodeView, UserLoginView, UserProfileView, UserUpdateView, UserBalanceView, \
    UserBalanceUpdateView, UserMessageView, UserWishlistView, UserPropertyView, UserTariffView, UserTransactionView, \
    UserSendMesageView
from apps.Views.filter_views import SearchProperty, PropertyView

urlpatterns = [
    path('auth/sendcode/', SendCodeView.as_view(), name='user_register'),
    path('auth/login/', UserLoginView.as_view(), name='user_login'),
]

urlpatterns += [
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/profile/update/', UserUpdateView.as_view(), name='user_profile_update'),
    path('user/profile/balance/', UserBalanceView.as_view(), name='user_balance'),
    path('user/profile/balance/update/', UserBalanceUpdateView.as_view(), name='user_balance_add'),
    path('user/profile/messages/', UserMessageView.as_view(), name='user_messages'),
    path('user/profile/wishlist/', UserWishlistView.as_view(), name='user_wishlist'),
    path('user/profile/listings/', UserPropertyView.as_view(), name='user_listings'),
    path('user/profile/tariff/', UserTariffView.as_view(), name='user_tariff'),
    path('user/profile/transactions/', UserTransactionView.as_view(), name='user_transactions'),
    path('user/profile/send/message/', UserSendMesageView.as_view(), name='user_send_message'),
]


urlpatterns += [
    path('search/', SearchProperty.as_view(), name='search_property'),
    path('property/<int:pk>', PropertyView.as_view(), name='property'),
]