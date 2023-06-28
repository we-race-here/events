from django.contrib.auth.mixins import UserPassesTestMixin


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
