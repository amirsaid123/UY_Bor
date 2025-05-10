from django.urls import path
from .views import *

urlpatterns = [
    path('data-update/', UserUpdateView.as_view(), name='data-update'),
    path('wishlist/<int:user_id>/', UserWishlistView.as_view(), name='user-wishlist'),
    path('blogs/', BlogListView.as_view(), name='blog-list'),

]
