# views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Organization
from .forms import OrganizationForm

class CreateOrganizationView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org/create_organization.html'

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'org/organization_detail.html'

class UpdateOrganizationView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org/update_organization.html'

class DeleteOrganizationView(DeleteView):
    model = Organization
    template_name = 'org/delete_organization.html'
    success_url = reverse_lazy('organizations')

class OrganizationListView(ListView):
    model = Organization
    template_name = 'org/organization_list.html'
    context_object_name = 'organizations'
    paginate_by = 10  # Change this to the desired number of items per page
