from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from events.users.permission_utils import StaffRequiredMixin

User = get_user_model()


class EmailsView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin/view_emails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["DJANGO_DEFAULT_FROM_EMAIL"] = settings.DJANGO_DEFAULT_FROM_EMAIL
        context["DO_NOT_REPLY"] = settings.DO_NOT_REPLY
        context["STAFF_EMAILS"] = settings.STAFF_EMAILS
        context["CALENDAR_EMAILS"] = settings.CALENDAR_EMAILS
        context["NOISY_EMAILS"] = settings.NOISY_EMAILS
        context["PREPEND_SUBJECT"] = settings.PREPEND_SUBJECT
        return context
