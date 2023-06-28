from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from events.users.permission_utils import StaffRequiredMixin

User = get_user_model()


class EmailsView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = "admin/view_emails.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
