from django import forms
from apps.event.models import Event
from django.forms import DateField, DateInput


class EventForm(forms.ModelForm):
    start_date = DateField(required=True, label="Date of Birth", widget=DateInput(attrs={'type': 'date', 'class': "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"}))

    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date']
