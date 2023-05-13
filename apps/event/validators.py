import csv
from typing import Literal

from django.contrib.auth import get_user_model
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist

from ..usac.models import UsacDownload

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
        category_validation: Literal["same", "mixed"] = "same",
        license_validation: bool = False,
        club_validation: bool = False,
    ):
        self.file = file
        self.category_validation = category_validation
        self.license_validation = license_validation
        self.club_validation = club_validation
        self.columns = None
        self.pii_fields = {"email", "phone", "address", "birth", "dob"}
        self.pii_columns = []
        self.data = []
        self.data_categories = set()
        self.errors = []
        self.warnings = []
        self.messages = []
        self.all_clubs = {j.get("club") for j in UsacDownload.objects.values("data")}

    def pii_check(self):
        """Check if pii field is in part of any column name.
        Does not need to be an exact match, just a substring match."""
        for col in self.columns:
            if any([pii in col.lower() for pii in self.pii_fields]):
                self.warnings.append(f"Column name {col} contains PII data")
                self.pii_columns.append(col)
        return self.pii_columns

    def check_columns(self):
        """Check if column names are valid"""
        errors = []
        if "Place" not in self.columns:
            errors.append('Column name "Place" is required')
        if "Category" not in self.columns:
            errors.append('Column name "Category" is required')
        if ("Name" not in self.columns) and (("First Name" not in self.columns) and ("Last Name" not in self.columns)):
            errors.append('Column name "Name" or "First Name" and "Last Name" is required')
        if self.license_validation and ("License" not in self.columns):
            errors.append('Column name "License" is required')
        if self.license_validation and ("Club" not in self.columns):
            errors.append('Column name "Club" is required USAC results. It may be blank')
        if self.license_validation and ("First Name" not in self.columns) and ("Last Name" not in self.columns):
            errors.append('Column name "First Name" and "Last Name" is required for USAC results')

        self.errors += errors
        return errors

    def usac_lookup(self, row):
        """Match user to results"""
        if "License" in self.columns and row["License"]:
            UsacDownload.objects.filter(license_number=row["License"])
        else:
            print(row["License"], row["_License"])
            return None

    def usac_club_lookup(self, row):
        """Match user to results"""
        rider = UsacDownload.objects.filter(license_number=row["license"])
        if rider and row["club"] in [c.lower() for c in rider.values_list("data", flat=True)]:
            return "matches_rider"
        elif row["club"] in self.all_clubs:
            return "Valid club, but does not match rider"
        else:
            return "Club not found in USAC database"

    def user_lookup(self, row):
        """Match user to results"""
        if "license" in self.columns and row["license"]:
            try:
                usac_license_match = User.objects.get(usac_license=row["license"])
                return serializers.serialize("json", usac_license_match)
            except ObjectDoesNotExist:
                return None
        else:
            return None

    def read_csv(self):
        """Read CSV file and return list of dictionaries"""
        reader = csv.DictReader(self.file, delimiter=",", quotechar='"')
        self.columns = reader.fieldnames
        reader.fieldnames = [col.strip().lower().replace(" ", "_") for col in reader.fieldnames]
        for row in reader:
            row = {k: v.strip().lower() for k, v in row.items()}
            self.data_categories.add(row["category"])
            try:
                row["place"] = int(row["place"])
                row["finish_status"] = "OK"
            except ValueError:
                row["finish_status"] = row["place"]
                row["palce"] = None
            if isinstance(row["license_number"], int):
                row["license_validation"] = self.usac_lookup(row)
            else:
                row["license_validation"] = row["license_number"]
            if self.club_validation:
                row["club_validation"] = self.usac_club_lookup(row)
            self.data_categories.add(row["category"])
        print(self.data_categories)
        # return self.data_categories


# def usac_license_on_record(license_number: str) -> str:
#     """Verifiy the USAC license number is on record at WRH and that it has been verified."""
#     try:
#         if license_number == "ONE DAY":
#             return "ONE DAY"
#         l = User.objects.get(usac_license_number=license_number)
#     except ObjectDoesNotExist:
#         return "FALSE"
#     except ValueError:
#         return "ERROR"
#     if l.usac_license_number_verified:
#         return "TRUE"
#     else:
#         return "NOT_VERIFIED"
#
#
# def valid_usac_licenses(license_number: str) -> str | list[str, ...]:
#     """Get status of USAC license number from USAC records (model)"""
#     try:
#         if license_number == "ONE DAY":
#             return "ONE DAY"
#         licenses = UsacDownload.objects.filter(license_number=license_number)
#         if not licenses:
#             return "NOT FOUND"
#         else:
#             return [f"{l.license_type}" for l in licenses if l.license_status.lower() == "valid"]
#     except ValueError:
#         return "ERROR"
#     except:
#         return "ERROR"
#
#
# def usac_club_match(license_number: str, club: str) -> str:
#     """Get status of persons USAC club from USAC records (model)"""
#     try:
#         if license_number == "ONE DAY":
#             return "ONE DAY"
#         if club == "":
#             return "NO CLUB"
#         licenses = UsacDownload.objects.filter(license_number=license_number)
#         if not licenses:
#             return "LICENSE NOT FOUND"
#         if club in [l.data["club"] for l in licenses]:
#             return "MATCH"
#         else:
#             return "NO MATCH"
#     except:
#         return "ERROR"
#
#
# def wrh_club_match(license_number: str, club: str) -> str:
#     """Get status of persons WRH club from WRH records (model)"""
#     try:
#         if license_number == "ONE DAY":
#             return "ONE DAY"
#         if club == "":
#             return "NO CLUB"
#         m = User.objects.get(usac_license_number=license_number)
#         clubs = OrganizationMember.objects.filter(member=m)
#         if clubs:
#             if club in [c.organization.name for c in clubs]:
#                 return "MATCH"
#             else:
#                 return "NO MATCH"
#     except ObjectDoesNotExist:
#         return "LICENSE NOT FOUND"
#     except:
#         return "ERROR"
#
#
# def wrh_bc_member(license_number: str) -> str:
#     """Get status of persons WRH BC from WRH records (model)"""
#     try:
#         m = User.objects.get(usac_license_number=license_number)
#         clubs = OrganizationMember.objects.filter(member=m)
#         if "Bicycle Colorado" in [c.organization.name for c in clubs]:
#             return "TRUE"
#         else:
#             return "FALSE"
#     except ObjectDoesNotExist:
#         return "LICENSE NOT FOUND"
#     except:
#         return "ERROR"
#
#
# def wrh_club_memberships(license_number: str) -> str:
#     try:
#         m = User.objects.get(usac_license_number=license_number)
#         clubs = OrganizationMember.objects.filter(member=m)
#         return [c.organization.name for c in clubs]
#     except ObjectDoesNotExist:
#         return ""
#     except:
#         return "ERROR"
#
#
# def wrh_email_match(email: str) -> str:
#     try:
#         m = User.objects.get(email=email)
#         return f"{m.first_name} {m.last_name}"
#     except ObjectDoesNotExist:
#         return "NOT FOUND"
#     except:
#         return "ERROR"
#
#
# def wrh_local_association(license_number: str) -> list[str] | str:
#     try:
#         m = UsacDownload.objects.filter(license_number=license_number)
#         return [t.local_association for t in m]
#     except:
#         return "ERROR"
#
#
# def wrh_usac_clubs(license_number: str) -> list[str] | str:
#     try:
#         m = UsacDownload.objects.filter(license_number=license_number)
#         return [t.data["club"] for t in m]
#     except:
#         return "ERROR"
#
#
# def bc_race_ready(license_number: str) -> Literal["TRUE", "FALSE"]:
#     usac_member = valid_usac_licenses(license_number) not in ["NOT FOUND", "ERROR", "ONE DAY"]
#     if usac_member:
#         return "TRUE"
#     else:
#         return "FALSE"
#
#
# def bc_individual_cup_ready(license_number: str) -> Literal["TRUE", "FALSE"]:
#     # TODO: need to check bc membership type.
#     if bc_race_ready == "TRUE" and wrh_bc_member(license_number) == "TRUE":
#         return "TRUE"
#     else:
#         return "FALSE"
#
#
# def bc_team_cup_ready(license_number: str, club: str) -> Literal["TRUE", "FALSE"]:
#     match_bc = wrh_club_match(license_number, club) == "MATCH"
#     # TODO: Should remove BC from the list.
#     match_usac = club in wrh_usac_clubs(license_number)
#     ind_ready = bc_individual_cup_ready(license_number) == "TRUE"
#     if match_bc and match_usac and ind_ready:
#         return "TRUE"
#     else:
#         return "FALSE"
