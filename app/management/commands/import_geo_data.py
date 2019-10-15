import csv
import os
from collections import defaultdict

from django.conf import settings
from django.core.management import BaseCommand, CommandError

from app.models import Position, Ship

IMOS_NAMES_MAP = {
    '9632179': 'Mathilde Maersk',
    '9247455': 'Australian Spirit',
    '9595321': 'MSC Preziosa'
}


class Command(BaseCommand):
    help = 'Imports geographical positions data related to 3 different ships.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='file',
            action='store',
            default=None,
            required=True,
            help='Absolute path to the file containing geographical data.'
        )

    def handle(self, *args, **options):
        try:
            self.stdout.write(
                self.style.SUCCESS('Starting importing geographical data...')
            )

            # Get the absolute path to the file containing geographic data
            # and construct the one-to-many (ship<-positions) relationship.
            data = defaultdict(list)
            file_path = os.path.join(settings.DATA_DIR, options['file'])
            with open(file_path, 'r') as fh:
                reader = csv.reader(fh)
                for row in reader:
                    imo, *positions = row
                    data[imo].append(positions)

            # Probably, the bigger CSV the bigger there urge to use
            # bulk_create/bulk_update.
            for imo, positions in data.items():
                ship, _ = Ship.objects.get_or_create(
                    imo=imo,
                    name=IMOS_NAMES_MAP.get(imo)
                )
                for timestamp, latitude, longitude in positions:
                    Position.objects.get_or_create(
                        latitude=latitude,
                        longitude=longitude,
                        ship=ship,
                        timestamp=timestamp,
                    )

            self.stdout.write(
                self.style.SUCCESS('The data has been imported successfully.')
            )
        except Exception as e:
            raise CommandError(e)
