from django.urls import path

from apps.usac.views import ImportCSV

app_name = "usac"

urlpatterns = [
    path("usac/importcsv", ImportCSV.as_view(), name="importcsv"),
]
