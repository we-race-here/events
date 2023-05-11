# urls.py
from django.urls import path

from .views import (
    BCAdminView,
    CreateOrganizationView,
    DeleteOrganizationView,
    JoinOrganizationView,
    OrganizationAdmin,
    OrganizationDetailView,
    OrganizationListView,
    UpdateOrganizationView,
)

app_name = "membership"

urlpatterns = [
    path("org", OrganizationListView.as_view(), name="organizations"),
    path("org/create/", CreateOrganizationView.as_view(), name="create_organization"),
    path("org/admin/<int:pk>/", OrganizationAdmin.as_view(), name="organization_admin"),
    path("org/<int:pk>/", OrganizationDetailView.as_view(), name="organization_detail"),
    path("org/<int:pk>/update/", UpdateOrganizationView.as_view(), name="update_organization"),
    path("org/<int:pk>/delete/", DeleteOrganizationView.as_view(), name="delete_organization"),
    path("org/join", JoinOrganizationView.as_view(), name="join_organization"),
    path("org/join/<int:organization_id>/", JoinOrganizationView.as_view(), name="join_organization_from_details"),
    path("bcadmin/", BCAdminView.as_view(), name="bcadmin"),
]
