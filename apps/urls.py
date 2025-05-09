from django.urls import path

from apps.views import SendCodeView, UserLoginView, UserProfileView, UserUpdateView

urlpatterns = [
    path('auth/sendcode/', SendCodeView.as_view(), name='user_register'),
    path('auth/login/', UserLoginView.as_view(), name='user_login'),
]

urlpatterns += [
    path('user/profile/', UserProfileView.as_view(), name='user_profile'),
    path('user/profile/update/', UserUpdateView.as_view(), name='user_profile_update'),
]