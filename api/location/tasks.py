from api.geosearch.celery import app
from api.location.models import Location, RequestHistory


@app.task(ignore_result=True)
def create_request_history(request_data):
    request, created = RequestHistory.objects.get_or_create(**request_data)
    if created:
        request.save()
