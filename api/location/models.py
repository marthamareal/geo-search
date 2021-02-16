from django.contrib.gis.db import models

from api.authentication.models import GeoUser


OPERATION_TYPE_CHOICES = (
    ('nearest', 'Nearest'),
    ('furthest', 'Furthest')
)


class Location(models.Model):
    point = models.PointField()


class RequestHistory(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    n = models.PositiveIntegerField()
    operation_type = models.CharField(max_length=8, choices=OPERATION_TYPE_CHOICES)
    user = models.ForeignKey(GeoUser, on_delete=models.CASCADE)
