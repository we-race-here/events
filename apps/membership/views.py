# views.py
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import OrganizationForm
from .models import Organization

User = get_user_model()


class CreateOrganizationView(LoginRequiredMixin, CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org/create_organization.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        if self.request.user.is_staff:
            form.instance.approved = True
        else:
            form.instance.approved = False
            # TODO: is it possible to get the Org id so that we can link to the org detail page from the email?
            html_message = render_to_string(
                "org/new_org_email.html",
                {
                    "TYPE": form.cleaned_data["type"],
                    "NAME": form.cleaned_data["name"],
                    "BYNAME": self.resquest.user.full_name,
                },
            )
            plain_message = strip_tags(html_message)
            # Thsi email is to the submitter
            send_mail(
                f"New {form.cleaned_data['type']} named: {form.cleaned_data['name']} is waiting approval",
                plain_message,
                "donotreply@bicyclecolorado.org",
                [self.request.user.email],
                html_message=html_message,
            )
            # This email is to the staff
            send_mail(
                f"New {form.cleaned_data['type']} named: {form.cleaned_data['name']} is waiting approval",
                plain_message,
                "donotreply@bicyclecolorado.org",
                [user.email for user in User.objects.filter(is_staff=True)],
                html_message=html_message,
            )
        return super().form_valid(form)


class OrganizationDetailView(DetailView):
    model = Organization
    template_name = "org/organization_detail.html"


class UpdateOrganizationView(LoginRequiredMixin, UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = "org/update_organization.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class DeleteOrganizationView(LoginRequiredMixin, DeleteView):
    model = Organization
    template_name = "org/delete_organization.html"
    success_url = reverse_lazy("organizations")


class OrganizationListView(ListView):
    model = Organization
    template_name = "org/organization_list.html"
    context_object_name = "organizations"
    paginate_by = 10  # Change this to the desired number of items per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type_choices"] = Organization.TYPE_CHOICES
        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        # Sorting
        sort_by = self.request.GET.get("sort", "")
        if sort_by:
            queryset = queryset.order_by(sort_by)
        search_query = self.request.GET.get("search", "")
        type_filter = self.request.GET.get("type", "")

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
                | Q(website__icontains=search_query)
                | Q(city__icontains=search_query)
                | Q(state__icontains=search_query)
            )

        if type_filter:
            queryset = queryset.filter(type=type_filter)

        return queryset
