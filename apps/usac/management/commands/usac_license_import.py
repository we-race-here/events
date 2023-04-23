import os
import sys

from django.core.management.base import BaseCommand

from apps.usac.admin import usac_license_from_csv


class Command(BaseCommand):
    help = "Import json data from Csv File"

    def add_arguments(self, parser):
        parser.add_argument('--input-file', action='store', required=True)

    def handle(self, *args, **options):
        input_file = options.get('input_file')
        if not os.path.exists(input_file):
            print('File [{}] does not exists!'.format(input_file))
            sys.exit(1)
        print('+++ Start Importing records from [{}] ...'.format(input_file))
        self._import_from_csv(input_file)
        print("+++ Finished!")

    def _import_from_csv(self, input_file):
        print('+++ starting....')
        with open(input_file, 'r') as csv_file:
            usac_license_from_csv(csv_file)

