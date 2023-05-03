import os
import sys

from django.core.management.base import BaseCommand

from apps.usac.admin import usac_license_from_csv


class Command(BaseCommand):
    help = "Import USAC data from Csv File"

    def add_arguments(self, parser):
        parser.add_argument("--input-file", action="store", required=True)

    def handle(self, *args, **options):
        input_file = options.get("input_file")
        if not os.path.exists(input_file):
            print(f"File [{input_file}] does not exists!")
            sys.exit(1)
        print(f"+++ Start Importing records from [{input_file}] ...")
        self._import_from_csv(input_file)
        print("+++ Finished!")

    def _import_from_csv(self, input_file):
        print("+++ starting....")
        with open(input_file) as csv_file:
            usac_license_from_csv(csv_file)
