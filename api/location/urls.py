from django.urls import path, include
from rest_framework import routers

from api.location.views import RequestHistoryViewSet, PointSearchViewSet

router = routers.DefaultRouter()

router.register(r'request_history', RequestHistoryViewSet, basename='request_history')
router.register(r'points', PointSearchViewSet, basename='points')

urlpatterns = [
    path('', include(router.urls)),
]
