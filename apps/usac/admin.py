import csv
from datetime import datetime
import io
import traceback

from django.contrib import admin
from django.shortcuts import render, redirect
from . import models
from .models import UsacDownload

from apps.usac.forms import CsvImportForm


# Register your models here.

class UsacDownloadAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'license_number', 'license_type', 'license_status',
                    'license_expiration')
    list_filter = ('license_type', 'license_status')
    search_fields = ('first_name', 'last_name', 'license_number')
    change_list_template = "admin/usac/usacdownload_changelist.html"

    def import_csv(self, request):
        context = {}
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]
            decoded_file = io.StringIO(csv_file.read().decode())
            try:
                import_rider_license_from_csv(decoded_file)
            except Exception as e:
                traceback.print_exc()
                context['error'] = str(e)
            else:
                self.message_user(request, "Your csv file has been imported")
                return redirect("..")
        form = CsvImportForm()
        context['form'] = form
        return render(
            request, "admin/csv_form.html", context
        )

def import_rider_license_from_csv(csv_file, date_format='%m/%d/%Y'):
    reader = csv.DictReader(csv_file)
    field_names = reader.fieldnames
    for i in range(len(field_names)):
        f = field_names[i].lower().replace('-', ' ')
        field_names[i] = '_'.join(f.split())
        if field_names[i] == 'license_#':
            field_names[i] = 'license_number'
        if field_names[i] == 'birthdate':
            field_names[i] = 'birth_date'

    required_fields = {
        'license_number', 'first_name', 'last_name', 'birth_date', 'race_age', 'race_gender', 'sex',
        'license_expiration', 'license_type', 'license_status', 'local_association'
    }
    missed_fields = required_fields - set(field_names)
    if missed_fields:
        raise Exception(f'Invalid csv file. missed this fields: {missed_fields}')
    for row in reader:
        # print(f'Importing row #{reader.line_num} ... ', end='')
        try:
            import_rider_license_row(row, required_fields, date_format=date_format)
            # print('[OK]' if obj else '[SKIP]')
        except Exception:
            # print('[FAIL]')
            traceback.print_exc()

def import_rider_license_row(row, required_fields, date_format='%m/%d/%Y'):
    row = {k: (v or None) for k, v in row.items()}
    if not row.get('license_number'):
        return
    data_hash = UsacDownload.hashify(row)
    if UsacDownload.objects.filter(data_hash=data_hash).exists():
        return
    db_cols = {c: row.get(c) for c in required_fields}
    if db_cols['birth_date']:
        db_cols['birth_date'] = datetime.strptime(db_cols['birth_date'], date_format)
    if db_cols['license_expiration']:
        db_cols['license_expiration'] = datetime.strptime(db_cols['license_expiration'], date_format)
    if db_cols['race_age']:
        db_cols['race_age'] = int(db_cols['race_age'])
    db_cols['data_hash'] = data_hash
    db_cols['data'] = row
    return UsacDownload.objects.create(**db_cols)


admin.site.register(models.UsacDownload, UsacDownloadAdmin)
