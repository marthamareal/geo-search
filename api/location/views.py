from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.location.models import RequestHistory, Location
from api.location.serializers import RequestHistorySerializer, LocationSerializer
from api.location.tasks import search_location_points, create_request_history


class RequestHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = RequestHistorySerializer
    permission_classes = (IsAuthenticated,)
    queryset = RequestHistory.objects.all()


class PointSearchViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Location.objects.all()

    @action(detail=False, methods=['get'])
    def get_locations(self, request, **kwargs):
        request_data = {}
        for param in ['x', 'y', 'n', 'operation_type']:
            if param not in request.GET:
                raise ValidationError({'error': '%s is required.' % param})

            request_data[param] = request.GET.get(param)

        if request_data:
            # add user to the request
            request_data['user_id'] = str(request.user.id)
            # Record request in history
            create_request_history.delay(request_data)
            # search Available locations
            results = search_location_points.delay(request_data)
            return Response(results.get(), status=status.HTTP_200_OK)
