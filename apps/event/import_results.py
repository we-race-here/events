import csv
from typing import BinaryIO, TextIO


class ImportResults:
    """
    filename: or file object
    categories: List of valid categories, maybe supplied by Race Model ot by user or None
    columns: List of columns in the file
    The file will be transformed into a list of dictionaries with the following keys
    place
    finish_status = models.CharField(max_length=16, default=FINISH_STATUS_OK, choices=FINISH_STATUS_CHOICES)
    category = models.CharField(max_length=32, null=True, blank=False)
    time = models.CharField(max_length=32, null=True, blank=True)
    gap = models.CharField(max_length=32, null=True, blank=True)
    bib_number = models.CharField(max_length=32, null=True, blank=True)
    usac_license = models.CharField(max_length=32, null=True, blank=True)
    club = models.CharField(max_length=256, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    more_data = models.JSONField(null=True, blank=True, )
    """

    def __init__(
        self, filename: str | BinaryIO | TextIO, dryrun: bool = True, categories: list = None, usac: bool = False
    ):
        self.filename = filename
        self.dryrun = dryrun
        self.categories = categories
        self.usac = usac
        self.columns = None
        self.ppi_fields = {"email", "phone", "address", "birth", "dob"}
        self.data = []
        self.errors = []
        self.messages = []

    def pii_check(self):
        """Check if pii field is in part of any column name.
        Does not need to be an exact match, just a substring match."""
        return [col for col in self.columns if [pii in col.lower() for pii in self.ppi_fields]]

    def check_columns_names(self):
        """Check if column names are valid"""
        if "Place" not in self.columns:
            self.errors.append('Column name "Place" is required')
        if "Category" not in self.columns:
            self.errors.append('Column name "Category" is required')
        if ("Name" not in self.columns) and (("First Name" not in self.columns) and ("Last Name" not in self.columns)):
            self.errors.append('Column name "Name" or "First Name" and "Last Name" is required')
        if "usac" and self.columns["License"] not in self.columns:
            self.errors.append('Column name "License" is required')
        if "usac" and self.columns["Team"] not in self.columns:
            self.errors.append('Column name "Team" is required')
        if "_finish_status" in self.columns:
            self.errors.append('Column name "_finish_status" is reserved')

        return [col for col in self.columns if [cat in col.lower() for cat in self.categories]]

    def import_results(self):
        # TODO: check if we have a file object or path
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            self.columns = reader.fieldnames
            for row in reader:
                pass
