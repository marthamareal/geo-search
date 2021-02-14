import csv

from django.contrib.gis.geos import Point
from django.core.management import BaseCommand

from api.location.models import Location


class Command(BaseCommand):
    help = 'Creates Locations in the db fro a given csv file'

    def handle(self, *args, **options):
        with open('points.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            # skip title row
            next(csv_reader)
            for row in csv_reader:
                # create location in the db
                Location.objects.create(id=row[0], point=Point(x=float(row[1]), y=float(row[2])))

        self.stdout.write(self.style.SUCCESS("All Location points are created"))
