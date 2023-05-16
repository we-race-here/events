import csv
from typing import Literal

from django.contrib.auth import get_user_model

# from ..usac.models import UsacDownload

# from django.core import serializers
# from django.core.exceptions import ObjectDoesNotExist


User = get_user_model()


class ImportResults:
    """
    filename: a form file decoded into a string
    categories: list or None: List of valid categories, maybe supplied by Race Model or by user
    columns: List of column names.
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
        self,
        file: list[str, ...],
        category_validation: Literal["same", "mixed", "rank"] = "mixed",
        is_usac: bool = True,
        license_validation: bool = False,
        club_validation: bool = False,
    ):
        self.file = file
        self.category_validation = category_validation
        self.is_usac = is_usac
        self.columns = None
        self.accepted_columns = [
            "name",
            "place",
            "category",
            "time",
            "gap",
            "bib_number",
            "usac_license",
            "club",
            "date_of_birth",
        ]
        self.reader = csv.DictReader(self.file, delimiter=",", quotechar='"')
        self.columns = self.normalize_fieldnames(self.reader.fieldnames)
        self.data = []
        self.data_categories = set()
        self.errors = []
        self.warnings = []
        self.messages = []

    def check_columns(self):
        """Check if column names are valid"""
        if "place" not in self.columns:
            self.errors.append('Column name "Place" is required')
        if "category" not in self.columns:
            self.errors.append('Column name "Category" is required')
        if ("name" not in self.columns) and (("first_name" not in self.columns) and ("last_name" not in self.columns)):
            self.errors.append('Column name "Name" or "First Name" and "Last Name" is required')
        if self.is_usac and ("usac_license" not in self.columns):
            self.errors.append('Column name "License" is required')
        if self.is_usac and ("club" not in self.columns):
            self.errors.append('Column name "Club" is required USAC results. It may be blank')
        if self.is_usac and ("first_name" not in self.columns) and ("last_name" not in self.columns):
            self.errors.append('Column name "First Name" and "Last Name" is required for USAC results')
        if not all(self.columns):
            self.errors.append("A column is blank in the header row")
        if self.errors:
            print(self.columns)

    def check_categories(self, req):
        if req == "same":
            if len(self.data_categories) > 1:
                self.errors.append("Multiple categories found")

    def normalize_fieldnames(self, fieldnames):
        """Normalize column names"""
        print(fieldnames)
        temp = [col.strip().lower().replace(" ", "_") for col in fieldnames]
        temp = [col.replace("dob", "date_of_birth") for col in temp]
        temp = [col.replace("bib", "bib_number") for col in temp]
        if "usac_license" not in temp:
            temp = [col.replace("license_number", "usac_license") for col in temp]
        if "usac_license" not in temp:
            temp = [col.replace("license", "usac_license") for col in temp]
        temp = [col.replace("team", "club") for col in temp]
        temp = [col.replace("club_name", "club") for col in temp]
        return temp

    def read_csv(self):
        """Read CSV file and return list of dictionaries"""
        # reader = csv.DictReader(self.file, delimiter=",", quotechar='"')
        self.reader.fieldnames = self.columns
        print(self.reader.fieldnames)
        for i, row in enumerate(self.reader):
            self.data_categories.add(row["category"])
            if any(row.values()):
                if row["place"] == "":
                    self.errors.append(f"Place is blank for# {i}")
                if row["category"] == "":
                    self.errors.append(f"Category is blank for# {i}")
                if row.get("name") == "" or (row.get("first_name") == "" and row.get("last_name") == ""):
                    self.errors.append(f"Name is blank for# {i}")
                if self.is_usac and row.get("usac_license") == "":
                    self.errors.append(f"License is blank for# {i}")
                try:
                    row["place"] = int(row["place"])
                    row["finish_status"] = "OK"
                except ValueError:
                    row["finish_status"] = row["place"]
                    row["palce"] = None
                self.data_categories.add(row["category"])
                if "name" not in self.columns:
                    row["name"] = f"{row['first_name']} {row['last_name']}"
                row["more_data"] = {k: v for k, v in row.items() if k not in self.accepted_columns}
                row = {k: v for k, v in row.items() if k in self.accepted_columns or k == "more_data"}
                self.data.append(row)
            else:
                self.errors.append(f"Error: Row {i} is blank")
