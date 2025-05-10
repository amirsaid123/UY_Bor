from django.urls import path
from apps.Views import *
from apps.Views.filter_views import *
from apps.Views.home_page_views import *

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
    path('user/profile/listings/deactivate/<int:pk>', UserDeactivatePropertyView.as_view(), name='deactivate_property')
]

urlpatterns += [
    path('search/', SearchProperty.as_view(), name='search_property'),
    path('property/<int:pk>', PropertyView.as_view(), name='property'),
]

urlpatterns += [
    path('vip/properties', VipPropertyView.as_view(), name='vip_property'),
    path('residential/complex/', ResidentialComplexView.as_view(), name='residential_complex'),
    path('videos/', VideoView.as_view(), name='videos'),
    path('blogs/', BlogView.as_view(), name='blogs'),
    path('static/pages', StaticPageView.as_view(), name='static_pages'),
]
