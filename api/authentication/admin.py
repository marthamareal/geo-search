from django.contrib import admin

# Register your models here.
from api.authentication.models import GeoUser

admin.site.register(GeoUser)
