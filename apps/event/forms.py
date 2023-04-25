from django import forms
from django.forms import Textarea
from apps.event.models import Event
from django.forms import DateField, DateInput


class EventForm(forms.ModelForm):
    start_date = DateField(required=True, label="Start Date", widget=DateInput(attrs={'type': 'date', 'class': "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"}))
    end_date = DateField(required=True, label="End Date", widget=DateInput(attrs={'type': 'date', 'class': "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"}))
    class Meta:
        model = Event
        fields = ['name', 'featured_event', 'blurb', 'description', 'start_date', 'end_date', 'email', 'website', 'registration_website',
                  'permit_no', 'is_usac_permitted', 'city', 'state', 'country', 'tags', 'panels', 'organization', 'publish_type', 'approved']
        widgets = {
            "name": Textarea(attrs={"cols": 80, "rows": 20}),
            "blurb": Textarea(attrs={"cols": 80, "rows": 100}),
            "description": Textarea(attrs={"cols": 80, "rows": 200}),
        }

