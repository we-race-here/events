import traceback

from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path

from apps.membership import models
from events.helpers import USACApi, admin_url_wrap


# Register your models here.
class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "organization", "is_active", "is_admin")
    list_filter = ("is_active", "is_admin", "organization")
    search_fields = ("user__first_name", "user__last_name", "organization__name")


# def get_urls(self):
# urls = super().get_urls()
# my_urls = [
#     path('<int:object_id>/validate-usac-license/',
#          admin_url_wrap(self.validate_usac_license, self.admin_site, self),
#          name="cycling_org_member_validate_usac_license"),
# ]
# return my_urls + urls
#
# def validate_usac_license(self, request, *args, **kwargs):
# object_id = kwargs.get('object_id')
# obj = self.get_object(request, object_id)
# if obj is None:
#     return self._get_obj_does_not_exist_redirect(
#         request, models.Member._meta, str(object_id)
#     )
# if not obj.usac_license_number:
#     self.message_user(request, '"usac_license_number" is not set for this member!', messages.WARNING)
#     return redirect("..")
# if obj.usac_license_number_verified:
#     self.message_user(request, '"usac_license_number" is already verified for this member!', messages.WARNING)
#     return redirect("..")
#
# if request.method == "POST":
#     obj.usac_license_number_verified = True
#     obj.save(update_fields=['usac_license_number_verified'])
#     self.message_user(request, f'"usac_license_number" verified for "{obj}" successfully.')
#     return redirect("..")
#
# error = None
# usac_object = None
# usac_api = USACApi({'user_id': settings.USAC_API_USERNAME, 'user_password': settings.USAC_API_PASSWORD})
# try:
#     usac_object = usac_api.lookup(license=obj.usac_license_number)
#     usac_object = usac_object[0] if usac_object else None
# except Exception as e:
#     traceback.print_exc()
#     error = str(e)
# if not usac_object:
#     error = f'No record matched with this usac_license_number "{obj.usac_license_number}"!'
#     matched = {}
# else:
#     matched = {
#         'name': (usac_object.get(
#             'profile_first_name') or '').lower() == f'{obj.first_name} {obj.last_name}'.lower(),
#         'age': usac_object.get('profile_birthdate') == obj.age,
#         'gender': (usac_object.get('profile_race_gender') or '').lower() == obj.get_gender_display().lower(),
#     }
# context = {
#     'object': obj,
#     'usac_object': usac_object,
#     'matched': matched,
#     'error': error,
#     **self.admin_site.each_context(request),
# }
# return render(
#     request, "admin/cycling_org/member_validate_usac_license.html", context
# )


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
