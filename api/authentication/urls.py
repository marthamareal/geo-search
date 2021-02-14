from django.urls import path

from api.authentication.views import RegistrationAPIView, LoginAPIView

urlpatterns = [
    path('users/signup/', RegistrationAPIView.as_view()),
    path('users/login/', LoginAPIView.as_view()),
]
