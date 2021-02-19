from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from api.authentication.views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    path('users/signup/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
