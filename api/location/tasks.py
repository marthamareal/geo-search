from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point

from api.geosearch.celery import app
from api.location.models import Location, RequestHistory
from api.location.serializers import LocationSerializer


@app.task()
def search_location_points(request_data):
    user_location = Point(float(request_data['x']), float(request_data['y']), srid=4326)
    locations = Location.objects.annotate(
        distance=Distance('point', user_location)
    )
    if request_data['operation_type'] == 'nearest':
        locations = locations.order_by('distance')[0:int(request_data['n'])]
    else:
        locations = locations.order_by('-distance')[0:int(request_data['n'])]
    return LocationSerializer(locations, many=True).data


@app.task(ignore_result=True)
def create_request_history(request_data):
    request = RequestHistory.objects.create(**request_data)
    request.save()

