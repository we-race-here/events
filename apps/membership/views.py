# views.py
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Organization
from .forms import OrganizationForm
from django.db.models import Q

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type_choices'] = Organization.TYPE_CHOICES
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get('search', '')
        type_filter = self.request.GET.get('type', '')

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(website__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(state__icontains=search_query)
            )

        if type_filter:
            queryset = queryset.filter(type=type_filter)

        return queryset
