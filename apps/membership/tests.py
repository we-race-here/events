from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.membership.models import Organization


class OrganizationURLTests(TestCase):
    def setUp(self):
        # Create a test user.
        self.test_user = get_user_model().objects.create_user(
            email="testuser@gmail.com",
            password="testpassword",
            is_staff=True,
        )

        # Log in the user
        logged_in = self.client.login(email="testuser@gmail.com", password="testpassword")

        # Check if the user is logged in
        self.assertTrue(logged_in)

        # Create an organization
        self.organization = Organization.objects.create(
            name="Test Organization",
            type="regional",
            blurb="This is a test organization",
            description="This is a description of a test organization",
            website="https://testorganization.com",
            email="test@testorganization.com",
            country="Test Country",
            city="Test City",
            state="Test State",
            zipcode="12345",
            membership_open=True,
            approved=True,
        )

    def test_organization_list_page_loads(self):
        response = self.client.get(reverse("membership:organizations"))
        self.assertEqual(response.status_code, 200)

    def test_create_organization_page_loads(self):
        form_data = {
            "name": "Test Organization",
            "type": "regional",
            "blurb": "This is a test organization",
            "description": "This is a description of a test organization",
            "website": "https://testorganization.com",
            "email": "test@testorganization.com",
            "country": "Test Country",
            "city": "Test City",
            "state": "Test State",
            "zipcode": "12345",
            "membership_open": True,
            "approved": True,
        }
        response = self.client.post(reverse("membership:create_organization"), form_data, follow=True)
        # If the form submission was successful, it should redirect or success.
        self.assertEqual(response.status_code, 200)

        # Check that the organization was created.
        self.assertEqual(Organization.objects.count(), 1)
        self.assertEqual(Organization.objects.first().name, "Test Organization")

    def test_organization_admin_page_loads(self):
        response = self.client.get(reverse("membership:organization_admin", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)

    def test_organization_detail_page_loads(self):
        response = self.client.get(reverse("membership:organization_detail", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_organization_page_loads(self):
        response = self.client.get(reverse("membership:update_organization", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)

    #
    def test_delete_organization_page_loads(self):
        response = self.client.get(reverse("membership:delete_organization", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)

    def test_join_organization_page_loads(self):
        response = self.client.get(reverse("membership:join_organization"))
        self.assertEqual(response.status_code, 200)

    #
    def test_join_organization_from_details_page_loads(self):
        response = self.client.get(reverse("membership:join_organization_from_details", args=[self.organization.id]))
        self.assertEqual(response.status_code, 200)

    #
    def test_clubs_admin_page_loads(self):
        response = self.client.get(reverse("membership:clubs_admin"))
        self.assertEqual(response.status_code, 200)
