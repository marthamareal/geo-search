from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.location.models import RequestHistory, Location
from api.location.serializers import RequestHistorySerializer, LocationSerializer
from api.location.tasks import search_location_points, create_request_history
from api.location.validators import validated_request_params


class RequestHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = RequestHistorySerializer
    permission_classes = (IsAuthenticated,)
    queryset = RequestHistory.objects.all()


class PointSearchViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()

    @action(detail=False, methods=['get'])
    def get_locations(self, request):
        request_data = validated_request_params(request)

        if request_data:
            # add user to the request
            request_data['user_id'] = str(request.user.id)
            # Record request in history
            create_request_history.delay(request_data)
            # # search Available locations
            user_location = Point(float(request_data['x']), float(request_data['y']), srid=4326)
            locations = Location.objects.annotate(
                distance=Distance('point', user_location)
            )
            if request_data['operation_type'] == 'nearest':
                locations = locations.order_by('distance')[0:int(request_data['n'])]
            else:
                locations = locations.order_by('-distance')[0:int(request_data['n'])]

            return Response(LocationSerializer(locations, many=True).data, status=status.HTTP_200_OK)
