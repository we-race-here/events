from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

from apps.membership.models import OrganizationMember


def is_org_admin(user):
    """
    Method to check if the logged-in user is an admin of the organization.

    Args:
    user (User): The logged-in user.
    org_id (int): The id of the organization to check.

    Returns:
    bool: True if the user is an admin of the organization, False otherwise.
    """
    status = OrganizationMember.objects.filter(Q(user=user) & (Q(is_admin=True)))
    return status


class StaffRequiredMixin(UserPassesTestMixin):
    """
    Mixin for class-based views to check if the logged-in user is staff.
    If the user is not staff, they will be redirected to the login page.
    """

    def test_func(self):
        """
        Method to check if the logged-in user is staff.

        Returns:
        bool: True if the user is staff, False otherwise.
        """
        return self.request.user.is_staff
