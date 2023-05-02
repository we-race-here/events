from django import forms
from django.contrib.postgres.forms import SimpleArrayField
from django.forms import CharField, DateField, DateInput, ModelChoiceField, Textarea, TimeField, TimeInput

from apps.event.models import Event, Race, RaceSeries


class UploadValidateFile(forms.Form):
    validate_file = forms.FileField()


class UploadRaceResults(forms.Form):
    event = ModelChoiceField(queryset=Event.objects.all())
    name = CharField(max_length=100)
    categories = SimpleArrayField(CharField(max_length=256))
    start_date = DateField(
        required=True,
        label="Start Date",
        widget=DateInput(
            attrs={
                "type": "Date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    start_time = TimeField(
        required=True,
        label="Start Time",
        widget=TimeInput(
            attrs={
                "type": "time",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    results_file = forms.FileField()


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
        fields = [
            "name",
            "featured_event",
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
            "panels",
            "organization",
            "publish_type",
            "approved",
        ]
        widgets = {
            "name": Textarea(attrs={"cols": 80, "rows": 20}),
            "blurb": Textarea(attrs={"cols": 80, "rows": 100}),
            "description": Textarea(attrs={"cols": 80, "rows": 200}),
        }


class RaceSeriesForm(forms.ModelForm):
    class Meta:
        model = RaceSeries
        fields = "__all__"


class ImportResults(forms.ModelForm):
    class Meta:
        model = Race
        fields = ["name", "event", "start_date", "start_time", "categories"]
