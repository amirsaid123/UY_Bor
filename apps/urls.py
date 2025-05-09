from django.urls import path

from apps.views import SendCodeView, UserLoginView

urlpatterns = [
    path('user/register/', SendCodeView.as_view(), name='user_register'),
    path('user/login/', UserLoginView.as_view(), name='user_login'),
]