from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.usac.admin import usac_license_from_csv
from apps.usac.forms import CsvImportForm
from events.users.permission_utils import StaffRequiredMixin


class ImportCSV(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    """Import CSV from USA c"""

    template_name = "import_csv.html"
    product_fields = ["name", ""]

    def post(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if self.request.POST.get("usacdownload", None):
            form = CsvImportForm(self.request.POST, self.request.FILES)
            if form.is_valid():
                csv_file = self.request.FILES["csv_file"]
                decoded_file = csv_file.read().decode("utf-8").splitlines()
                context.update(usac_license_from_csv(decoded_file))
                return self.render_to_response(context)
        form = CsvImportForm()
        context.update({"form": form})
        return self.render_to_response(context)

    def get(self, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = CsvImportForm()
        context.update({"form": form})
        return self.render_to_response(context)
