import os

from celery.app import Celery

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.geosearch.settings')

app = Celery('geosearch')

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
