# urls.py
from django.urls import path
from .views import OrganizationListView, CreateOrganizationView, OrganizationDetailView, UpdateOrganizationView, DeleteOrganizationView

urlpatterns = [
    path('org', OrganizationListView.as_view(), name='organizations'),
    path('org/create/', CreateOrganizationView.as_view(), name='create_organization'),
    path('org/<int:pk>/', OrganizationDetailView.as_view(), name='organization_detail'),
    path('org/<int:pk>/update/', UpdateOrganizationView.as_view(), name='update_organization'),
    path('org/<int:pk>/delete/', DeleteOrganizationView.as_view(), name='delete_organization'),
]
