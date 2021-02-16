from django.contrib import admin

from api.location.models import Location, RequestHistory

admin.site.register(Location)
admin.site.register(RequestHistory)
