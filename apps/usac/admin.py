import csv
import functools
import hashlib
import io
import json
import traceback
from datetime import datetime

from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path

from apps.usac.forms import CsvImportForm

from . import models
from .models import UsacDownload


def admin_url_wrap(view, admin_site, model_admin=None):
    def wrapper(*args, **kwargs):
        return admin_site.admin_view(view)(*args, **kwargs)

    wrapper.model_admin = model_admin
    return functools.update_wrapper(wrapper, view)


# Register your models here.


class UsacDownloadAdmin(admin.ModelAdmin):
    """This defiens the table view of usac recrods"""

    list_display = (
        "id",
        "first_name",
        "last_name",
        "license_number",
        "license_type",
        "license_status",
        "license_expiration",
    )
    list_filter = ("license_type", "license_status")
    search_fields = ("first_name", "last_name", "license_number")
    change_list_template = "admin/usac/usacdownload_changelist.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                "import-csv/",
                admin_url_wrap(self.import_csv, self.admin_site, self),
                name="usacycling_riderlicense_importcsv",
            ),
        ]
        return my_urls + urls

    def import_csv(self, request):
        """This is the form to import records from a csv"""
        context = {}
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_file = io.StringIO(csv_file.read().decode())
            try:
                usac_license_from_csv(decoded_file)
            except Exception as e:
                traceback.print_exc()
                context["error"] = str(e)
            else:
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        form = CsvImportForm()
        context["form"] = form
        return render(request, "admin/csv_form.html", context)


def hashify_row(row: dict) -> str:
    row = json.dumps(row, sort_keys=True, default=str)
    return hashlib.sha1(row.encode()).hexdigest()


def usac_license_from_csv(csv_object):
    """This is for importing usac records from racerdownload a csv"""
    date_format = "%m/%d/%Y"
    errors = []

    def field_map(f: str) -> str:
        return f.lower().strip().replace(" ", "_").replace("#", "number").replace("birthdate", "birth_date")

    # These are the model fields, except for the json extra fields
    required_fields = {
        "license_number",
        "first_name",
        "last_name",
        "birth_date",
        "race_age",
        "race_gender",
        "sex",
        "license_expiration",
        "license_type",
        "license_status",
        "local_association",
    }
    reader = csv.DictReader(csv_object)
    reader.fieldnames = [field_map(f) for f in reader.fieldnames]
    try:
        assert required_fields.intersection(reader.fieldnames) == required_fields
    except:
        # print(required_fields.intersection(_fieldnames).difference(required_fields))
        raise Exception(
            f"Missing required fields: {required_fields.intersection(reader.fieldnames).difference(required_fields)}"
        )
    try:
        assert "license_number" in reader.fieldnames
    except:
        # print("license_number not in fieldnames: [f for f in _fieldnames if 'license' in f.lower)]")
        raise Exception("license_number not in fieldnames")
    hash_set = set(UsacDownload.objects.values_list("data_hash", flat=True))
    bulk_list = []
    attempted = 0
    duplicates = 0
    rows_created = 0
    for row in reader:
        attempted += 1
        try:
            try:
                row["birth_date"] = datetime.strptime(row["birth_date"], date_format)
            except:
                errors.append(f"Invalid birth_date: {row['license_number']}: {row['birth_date']}")
                row["birth_date"] = None
            try:
                row["license_expiration"] = datetime.strptime(row["license_expiration"], date_format)
            except:
                errors.append(f"Invalid license_expiration: {row['license_number']}: {row['license_expiration']}")
                row["license_expiration"] = None
            if not row["license_number"]:
                errors.append(f"Invalid license_number: {row['last_name']}, {row['first_name']}")
                continue
            reqs = {k.strip(): (v or None) for k, v in row.items() if k in required_fields}
            extra = {k.strip(): (v or None) for k, v in row.items() if k not in required_fields}
            data_hash = {}
            data_hash.update(reqs)
            data_hash.update(extra)
            reqs["data_hash"] = hashify_row(data_hash)
            if reqs["data_hash"] in hash_set:
                duplicates += 1
                continue
            reqs.update({"data": extra})
            bulk_list.append(UsacDownload(**reqs))
        except Exception as e:
            errors.append(f"Unknown Error: {row['license_number']}")
            raise e
    try:
        # return UsacDownload.objects.create(**row)
        created = UsacDownload.objects.bulk_create(bulk_list, batch_size=1000, ignore_conflicts=True)
        rows_created += len(created)
    except Exception as e:
        raise Exception(f"Error: {e}")
    return {
        "attempted": attempted,
        "duplicates": duplicates,
        "errors": errors,
        "rows_created": rows_created,
    }


admin.site.register(models.UsacDownload, UsacDownloadAdmin)
