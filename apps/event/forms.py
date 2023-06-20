from django import forms
from django.contrib.auth import get_user_model
from django.forms import CharField, DateField, DateInput, ModelChoiceField, ModelForm, TimeField, TimeInput

from apps.event.models import Event, Race, RaceResult, RaceSeries

from .models import event_types

User = get_user_model()


class UploadValidateFile(forms.Form):
    validate_file = forms.FileField()


class RaceResultsImport(forms.Form):
    name = CharField(max_length=100, label="Race Name")
    # event = ModelChoiceField(queryset=Event.objects.all(), label="Choose and Event")
    raceseries = ModelChoiceField(queryset=RaceSeries.objects.all(), label="Select a Race Series(s)")
    category_validation = forms.ChoiceField(
        required=False, choices=(("same", "Same"), ("mixed", "Mixed")), label="Category validation"
    )
    is_usac = forms.BooleanField(required=False, label="Is a USAC race")
    start_date = DateField(
        required=True,
        label="Start Date",
        widget=DateInput(
            attrs={
                "type": "Date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 "
                "placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none "
                "focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    start_time = TimeField(
        required=False,
        label="Start Time (optional)",
        widget=TimeInput(
            attrs={
                "type": "time",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 "
                "placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none "
                "focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    results_file = forms.FileField()


class EventForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=event_types,
        required=False,
    )
    start_date = DateField(
        required=True,
        label="Start Date",
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 "
                "placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none "
                "focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    end_date = DateField(
        required=True,
        label="End Date",
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 "
                "placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none "
                "focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "ckeditor"}))

    class Meta:
        model = Event
        css = (
            "block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 "
            "appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none "
            "focus:ring-0 focus:border-blue-600 peer"
        )
        fields = [
            "name",
            "blurb",
            "description",
            "logo",
            "hero",
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
            "name": forms.TextInput(attrs={"class": css}),
            "blurb": forms.TextInput(attrs={"class": css}),
            "start_date": forms.Textarea(attrs={"class": css}),
            "email": forms.TextInput(attrs={"class": css}),
            "website": forms.TextInput(attrs={"class": css}),
            "registration_website": forms.TextInput(attrs={"class": css}),
            "permit_no": forms.TextInput(attrs={"class": css}),
            "city": forms.TextInput(attrs={"class": css}),
            "state": forms.TextInput(attrs={"class": css}),
            "country": forms.TextInput(attrs={"class": css}),
            # "tags": forms.SelectMultiple(attrs={"class": css}, choices=event_types),
        }


class RaceSeriesForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Event.objects.all().order_by("name")
    )

    class Meta:
        model = RaceSeries
        ordering = ["name"]
        fields = [
            "organization",
            "name",
            "description",
            "logo",
            "categories",
            "points_map",
            "point_system",
            "events",
        ]
        # widgets = {"events": forms.CheckboxSelectMultiple(choices=Event.objects.all().order_by("name"))}


class AddEventToRaceSeriesForm(forms.ModelForm):
    pass


class ImportResults(forms.ModelForm):
    class Meta:
        model = Race
        fields = ["name", "event", "start_date", "start_time", "categories"]


class RaceForm(forms.ModelForm):
    race_series = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=RaceSeries.objects.all().order_by("name")
    )
    event = forms.ModelChoiceField(widget=forms.CheckboxInput, queryset=Event.objects.all().order_by("name"))

    class Meta:
        model = Race
        fields = ["name", "event", "start_date", "start_time", "categories", "race_series"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "categories": forms.TextInput(attrs={"class": "form-control"}),
        }


class RaceResultForm(ModelForm):
    rider = forms.ModelChoiceField(widget=forms.CheckboxInput, queryset=User.objects.all().order_by("last_name"))
    race = forms.ModelChoiceField(widget=forms.CheckboxInput, queryset=Race.objects.all().order_by("start_date"))

    class Meta:
        model = RaceResult
        fields = [
            "rider",
            "name",
            "race",
            "place",
            "finish_status",
            "category",
            "time",
            "gap",
            "bib_number",
            "usac_license",
            "club",
            "date_of_birth",
            "more_data",
        ]
        widgets = {
            "name": forms.TextInput(),
            "place": forms.NumberInput(),
            "finish_status": forms.TextInput(),
            "category": forms.TextInput(),
            "time": forms.TextInput(),
            "gap": forms.TextInput(),
            "bib_number": forms.TextInput(),
            "usac_license": forms.TextInput(),
            "club": forms.TextInput(),
            "date_of_birth": forms.DateInput(),
            "more_data": forms.TextInput(),
        }
