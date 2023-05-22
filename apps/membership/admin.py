from django.contrib import admin

from apps.membership import models


# Register your models here.
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "organization", "is_active", "is_admin")
    list_filter = ("is_active", "is_admin", "organization")
    search_fields = ("user__first_name", "user__last_name", "organization__name")


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "type",
        "website",
    )
    search_fields = ("name", "website", "email", "phone")
    list_filter = ("type",)


admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.OrganizationMember, OrganizationMemberAdmin)
