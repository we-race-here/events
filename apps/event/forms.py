from django import forms
from django.forms import DateField, DateInput, Textarea

from apps.event.models import Event, RaceSeries


class EventForm(forms.ModelForm):
    start_date = DateField(
        required=True,
        label="Start Date",
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    end_date = DateField(
        required=True,
        label="End Date",
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )

    class Meta:
        model = Event
        css = "block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
        fields = [
            "name",
            "blurb",
            "description",
            "start_date",
            "end_date",
            "email",
            "website",
            "registration_website",
            "permit_no",
            "is_usac_permitted",
            "city",
            "state",
            "country",
            "tags",
            "organization",
            "publish_type",
            "featured_event",
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': css}),
            'blurb': forms.TextInput(attrs={'class': css}),
            'description': forms.Textarea(attrs={'class': css}),
            'start_date': forms.Textarea(attrs={'class': css}),
            'email': forms.TextInput(attrs={'class': css}),
            'website': forms.TextInput(attrs={'class': css}),
            'registration_website': forms.TextInput(attrs={'class': css}),
            'permit_no': forms.TextInput(attrs={'class': css}),
            'city': forms.TextInput(attrs={'class': css}),
            'state': forms.TextInput(attrs={'class': css}),
            'country': forms.TextInput(attrs={'class': css}),
            'tags': forms.TextInput(attrs={'class': css}),

        }


class RaceSeriesForm(forms.ModelForm):
    class Meta:
        model = RaceSeries
        fields = "__all__"
