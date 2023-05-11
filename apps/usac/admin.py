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


def usac_license_from_csv(csv_file, date_format="%m/%d/%Y"):
    "This is the import logic"
    reader = csv.DictReader(csv_file)
    field_names = reader.fieldnames
    for i in range(len(field_names)):
        f = field_names[i].lower().replace("-", " ")
        field_names[i] = "_".join(f.split())
        if field_names[i] == "license_#":
            field_names[i] = "license_number"
        if field_names[i] == "birthdate":
            field_names[i] = "birth_date"

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
    missed_fields = required_fields - set(field_names)
    if missed_fields:
        raise Exception(f"Invalid csv file. missed this fields: {missed_fields}")
    for row in reader:
        # print(f'Importing row #{reader.line_num} ... ', end='')
        try:
            import_usac_license_row(row, required_fields, date_format=date_format)
            # print('[OK]' if obj else '[SKIP]')
        except Exception:
            # print('[FAIL]')
            traceback.print_exc()


def import_usac_license_row(row, required_fields, date_format="%m/%d/%Y"):
    """This is the import logic per row"""
    row = {k: (v or None) for k, v in row.items()}
    if not row.get("license_number"):
        return
    data_hash = UsacDownload.hashify(row)
    try:
        if UsacDownload.objects.filter(data_hash=data_hash).exists():
            return
    except:
        return
    db_cols = {c: row.get(c) for c in required_fields}
    if db_cols["birth_date"]:
        try:
            db_cols["birth_date"] = datetime.strptime(db_cols["birth_date"], date_format)
        except ValueError:
            # print(f"Invalid birth date: {db_cols['birth_date']}")
            db_cols["birth_date"] = None
    if db_cols["license_expiration"]:
        try:
            db_cols["license_expiration"] = datetime.strptime(db_cols["license_expiration"], date_format)
        except ValueError:
            # print(f"license_expiration: {db_cols['license_expiration']}")
            db_cols["birth_date"] = None
    if db_cols["race_age"]:
        db_cols["race_age"] = int(db_cols["race_age"])
    db_cols["data_hash"] = data_hash
    db_cols["data"] = row
    return UsacDownload.objects.create(**db_cols)


admin.site.register(models.UsacDownload, UsacDownloadAdmin)


def hashify_extra(extra: dict) -> str:
    extra = json.dumps(extra, sort_keys=True)
    return hashlib.sha1(extra.encode()).hexdigest()


def new_usac_import(csv_object):
    """This is for importing usac records from racerdownload a csv"""
    date_format = "%m/%d/%Y"
    errors = []

    def field_map(f: str) -> str:
        return f.lower().strip().replace(" ", "_").replace("#", "number").replace("birthdate", "birth_date")

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
    bulk_list = []
    success = 0
    attempted = 0
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
                errors.append(f"Invalid license_number: {row['license_number']}")
                continue
            reqs = {k: (v or None) for k, v in row.items() if k in required_fields}
            extra = json.dumps({k: (v or None) for k, v in row.items() if k not in required_fields}, sort_keys=True)
            reqs["data_hash"] = hashlib.sha1(extra.encode()).hexdigest()
            reqs.update({"data": extra})
            bulk_list.append(UsacDownload(**reqs))
            success += 1
        except:
            errors.append(f"Unknown Error: {row['license_number']}")
    try:
        rows_created = UsacDownload.objects.bulk_create(bulk_list, batch_size=1000, ignore_conflicts=True)
    except Exception as e:
        raise Exception(f"Error: {e}")
    total = success + attempted
    return {
        "total": total,
        "success": success,
        "attempted": attempted,
        "errors": errors,
        "rows_created": len(rows_created),
    }
