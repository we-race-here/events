# urls.py
from django.urls import path

from .views import (
    ClubAdmin,
    CreateOrganizationView,
    DeleteOrganizationView,
    JoinOrganizationView,
    OrganizationAdmin,
    OrganizationDetailView,
    ClubListView,
    UpdateOrganizationView,
    PromoterListView,
)

app_name = "membership"

urlpatterns = [
    path("org", ClubListView.as_view(), name="organizations"),
    path("promoters", PromoterListView.as_view(), name="promoters"),
    path("org/create/", CreateOrganizationView.as_view(), name="create_organization"),
    path("org/admin/<int:pk>/", OrganizationAdmin.as_view(), name="organization_admin"),
    path("org/<int:pk>/", OrganizationDetailView.as_view(), name="organization_detail"),
    path("org/<int:pk>/update/", UpdateOrganizationView.as_view(), name="update_organization"),
    path("org/<int:pk>/delete/", DeleteOrganizationView.as_view(), name="delete_organization"),
    path("org/join", JoinOrganizationView.as_view(), name="join_organization"),
    path("org/join/<int:organization_id>/", JoinOrganizationView.as_view(), name="join_organization_from_details"),
    path("org/clubs_admin/", ClubAdmin.as_view(), name="clubs_admin"),
]
