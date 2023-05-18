from django.contrib import admin

from apps.event import models


# Register your models here.
class RaceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "event",
        "start_date",
    )
    search_fields = (
        "name",
        "event__name",
        "categories",
    )
    list_filter = ("start_date",)


class RaceResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "race",
        "rider",
        "name",
        "place",
        "place_disp",
        "category",
        "usac_license",
        "club",
    )
    search_fields = ("race__name", "rider__first_name", "rider__last_name", "name", "club", "category")
    # list_filter = ("race",)


class RaceSeriesAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "organization",
        "point_system",
        "categories",
    )
    search_fields = ("name",)
    list_filter = ("organization",)


class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "start_date", "is_usac_permitted", "featured_event", "city", "organization")
    search_fields = ("name",)
    list_filter = ("is_usac_permitted", "featured_event", "organization")


admin.site.register(models.Race, RaceAdmin)
admin.site.register(models.RaceResult, RaceResultAdmin)
admin.site.register(models.RaceSeries, RaceSeriesAdmin)
admin.site.register(models.Event, EventAdmin)
