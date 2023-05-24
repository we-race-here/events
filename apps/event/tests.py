from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from apps.event.models import Event
from django.contrib.auth import get_user_model
from apps.membership.models import Organization


class URLLoadingTest(TestCase):

    def setUp(self):
        # Create a test user.
        self.test_user = get_user_model().objects.create_user(
            email="testuser@gmail.com",
            password='testpassword',
            is_staff=True,
        )

        # Log in the user
        logged_in = self.client.login(email='testuser@gmail.com', password='testpassword')

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

        self.EVENT_PAYLOAD = {
            'name': 'Test Event',
            'blurb': 'This is a test event.',
            'description': 'A much longer description for the test event.',
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'email': 'test@example.com',
            'website': 'http://example.com',
            'registration_website': 'http://example.com/register',
            'permit_no': '12345',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'organization': self.organization,
            'publish_type': 'public'
        }

        self.EVENT = Event.objects.create(**self.EVENT_PAYLOAD)
    # Home Pages
    def test_home_page_loads(self):
        response = self.client.get(reverse('home')) # Assume 'home' is the name of your url pattern for the home page
        self.assertEqual(response.status_code, 302)

    def test_homepage_loads(self):
        response = self.client.get(reverse('homepage')) # Assume 'homepage' is the name of your url pattern for the home page
        self.assertEqual(response.status_code, 200)

    # Events
    def test_event_list_page_loads(self):
        response = self.client.get(reverse('event:event_list'))
        self.assertEqual(response.status_code, 200)

    def test_event_create_page_loads(self):
        response = self.client.get(reverse('event:event_create'))
        self.assertEqual(response.status_code, 200)

        # Assuming some valid form data
        form_data = {
            'name': 'Test Event 1',
            'blurb': 'This is a test event.',
            'description': 'A much longer description for the test event.',
            'start_date': '2023-01-01',
            'end_date': '2023-01-02',
            'email': 'test@example.com',
            'website': 'http://example.com',
            'registration_website': 'http://example.com/register',
            'permit_no': '12345',
            'city': 'Test City',
            'state': 'Test State',
            'country': 'Test Country',
            'organization': self.organization.id,
            'publish_type': 'public'
        }

        response = self.client.post(reverse('event:event_create'), form_data)
        # If the form submission is successful, Django should redirect to a new URL.
        # We'll assume here that it redirects to the event list page.
        self.assertRedirects(response, reverse('event:event_list'))

        # You can also test that an Event object was created in the database.
        # Replace Event with the actual name of your Event model.
        event = Event.objects.get(name='Test Event 1')
        self.assertIsNotNone(event)
        # And that the fields on the event are what we expect.
        self.assertEqual(event.blurb, 'This is a test event.')



    def test_event_detail_page_loads(self):
        response = self.client.get(reverse('event:event_detail', args=[self.EVENT.id]))
        self.assertEqual(response.status_code, 200)
    #
    def test_event_update_page_loads(self):
        response = self.client.get(reverse('event:event_update', args=[self.EVENT.id]))
        self.assertEqual(response.status_code, 200)
    #
    def test_event_delete_page_loads(self):
        response = self.client.get(reverse('event:event_delete', args=[self.EVENT.id]))
        self.assertEqual(response.status_code, 200)
    #
    def test_import_race_results_page_loads(self):
        response = self.client.get(reverse('event:import_race_results', args=[self.EVENT.id]))
        self.assertEqual(response.status_code, 200)
    #
    def test_events_results_list_page_loads(self):
        response = self.client.get(reverse('event:events_results_list'))
        self.assertEqual(response.status_code, 200)

    def test_raceseries_detail_page_loads(self):
        response = self.client.get(reverse('event:raceseries_detail', args=[self.EVENT.id]))
        self.assertEqual(response.status_code, 404)

    def test_raceseries_create_page_loads(self):
        response = self.client.get(reverse('event:raceseries_create'))
        self.assertEqual(response.status_code, 200)
    #
    def test_raceseries_update_page_loads(self):
        response = self.client.get(reverse('event:raceseries_update', args=[self.EVENT.id]))
        self.assertEqual(response.status_code, 404)
    #
    def test_race_create_page_loads(self):
        response = self.client.get(reverse('event:race_create'))
        self.assertEqual(response.status_code, 200)
    #
    def test_raceresult_create_page_loads(self):
        response = self.client.get(reverse('event:raceresult_create'))
        self.assertEqual(response.status_code, 200)

# python manage.py test apps.event.tests.URLLoadingTest
# python manage.py test apps.membership.tests.OrganizationURLTests
