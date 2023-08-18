from datetime import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.forms import (
    CharField,
    DateField,
    DateInput,
    ModelChoiceField,
    ModelForm,
    TimeField,
    TimeInput,
    TextInput,
    SelectMultiple,
    FileInput,
)
from django.forms.widgets import Textarea, SelectDateWidget, Select, CheckboxInput
from turnstile.fields import TurnstileField

from apps.membership.models import Organization
from config.helpers.widgets import GoogleMapsWidget
from .models import Event, Race, RaceResult, RaceSeries, event_types

User = get_user_model()

STATE_CHOICES = [
    ("AL", "Alabama"),
    ("AK", "Alaska"),
    ("AZ", "Arizona"),
    ("AR", "Arkansas"),
    ("CA", "California"),
    ("CO", "Colorado"),
    ("CT", "Connecticut"),
    ("DE", "Delaware"),
    ("FL", "Florida"),
    ("GA", "Georgia"),
    ("HI", "Hawaii"),
    ("ID", "Idaho"),
    ("IL", "Illinois"),
    ("IN", "Indiana"),
    ("IA", "Iowa"),
    ("KS", "Kansas"),
    ("KY", "Kentucky"),
    ("LA", "Louisiana"),
    ("ME", "Maine"),
    ("MD", "Maryland"),
    ("MA", "Massachusetts"),
    ("MI", "Michigan"),
    ("MN", "Minnesota"),
    ("MS", "Mississippi"),
    ("MO", "Missouri"),
    ("MT", "Montana"),
    ("NE", "Nebraska"),
    ("NV", "Nevada"),
    ("NH", "New Hampshire"),
    ("NJ", "New Jersey"),
    ("NM", "New Mexico"),
    ("NY", "New York"),
    ("NC", "North Carolina"),
    ("ND", "North Dakota"),
    ("OH", "Ohio"),
    ("OK", "Oklahoma"),
    ("OR", "Oregon"),
    ("PA", "Pennsylvania"),
    ("RI", "Rhode Island"),
    ("SC", "South Carolina"),
    ("SD", "South Dakota"),
    ("TN", "Tennessee"),
    ("TX", "Texas"),
    ("UT", "Utah"),
    ("VT", "Vermont"),
    ("VA", "Virginia"),
    ("WA", "Washington"),
    ("WV", "West Virginia"),
    ("WI", "Wisconsin"),
    ("WY", "Wyoming"),
]


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


############################################################################################################
# Event Forms
############################################################################################################
event_fields = {
    "turnstile": TurnstileField(label=""),
    "description": forms.CharField(
        label="Event Description",
        max_length=2500,
        required=False,
        widget=forms.Textarea(
            attrs={
                # "class": "editor-basic",
                "class": "fb_text_area_field",
                "rows": 10,
                "placeholder": "A longer event description with basic formatting and links (2500 characters max)",
            },
        ),
    ),
    "user_first": forms.CharField(
        label="First Name",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "last name",
            },
        ),
    ),
    "user_last": forms.CharField(
        label="Last Name",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "last name",
                "max_length": 50,
            }
        ),
    ),
    "user_email": forms.EmailField(
        label="Your Email Address",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "your emails address",
                "max_length": 75,
            }
        ),
    ),
    "name": forms.CharField(
        label="Event Name",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Name of the event",
                "max_length": 75,
            }
        ),
    ),
    "email": forms.EmailField(
        label="Event Contact Email Address",
        required=False,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "emails address",
                "max_length": 75,
            }
        ),
    ),
    "tags": forms.MultipleChoiceField(
        label="Select Event Tag(s) or Type(s)",
        required=True,
        choices=event_types,
        widget=SelectMultiple(
            attrs={"class": "fb_select_multiple", "placeholder": "Event tags and type", "help_text": "select multiple"}
        ),
    ),
    "logo": forms.CharField(
        label="Event logo",
        required=False,
        widget=FileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer "
                "focus:outline-none"
            }
        ),
    ),
    "hero": forms.CharField(
        label="Event banner image",
        required=False,
        widget=FileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer "
                "focus:outline-none"
            }
        ),
    ),
    "blurb": forms.CharField(
        label="Short Description",
        required=True,
        widget=Textarea(
            attrs={
                "class": "fb_text_area_field",
                "placeholder": "short description of the event (250 characters max)",
                "rows": 4,
                "max_length": 50,
            },
        ),
    ),
    "start_date": forms.DateField(
        initial=datetime.now(),
        required=True,
        widget=SelectDateWidget(
            attrs={"class": "fb_select_date_field"},
            years=range(datetime.now().year, datetime.now().year + 3),
        ),
    ),
    "end_date": forms.DateField(
        initial=datetime.now(),
        required=True,
        widget=SelectDateWidget(
            attrs={"class": "fb_select_date_field"},
            years=range(datetime.now().year, datetime.now().year + 3),
        ),
    ),
    "website": forms.URLField(
        label="Event website or other URL. Include https://...",
        required=False,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Website, Facebook, or other URL",
                "max_length": 100,
            }
        ),
    ),
    "registration_website": forms.URLField(
        label="Registration website. Include https://...",
        required=False,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "bikereg, or other URL",
                "max_length": 100,
            }
        ),
    ),
    "city": forms.CharField(
        label="Nearest City",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Name of the nearest city",
                "max_length": 75,
            }
        ),
    ),
    "state": forms.ChoiceField(
        initial="CO",
        label="Event State",
        required=True,
        choices=STATE_CHOICES,
        widget=Select(attrs={"class": "fb_select_multiple", "placeholder": "Event State"}),
    ),
    "is_permitted": forms.BooleanField(
        initial=False, label="USAC Permited", required=False, widget=CheckboxInput(attrs={"class": "fb_checkbox_field"})
    ),
    "permit_no": forms.CharField(
        label="Permit Number",
        required=False,
        widget=TextInput(attrs={"class": "fb_text_input_field", "placeholder": "123"}),
    ),
    "featured_event": forms.BooleanField(
        required=False,
        label="Featured (Payment Required)",
        initial=False,
        widget=CheckboxInput(attrs={"class": "fb_checkbox_field"}),
    ),
    "publish_type": forms.ChoiceField(
        initial="public",
        label="Publish (sharing) options",
        required=True,
        choices=Event.PUBLISH_TYPE_CHOICES,
        widget=Select(attrs={"class": "fb_select_multiple", "placeholder": "Sharing Options"}),
    ),
    "approved": forms.BooleanField(
        label="Approve the event to be published",
        initial=False,
        required=False,
        widget=CheckboxInput(attrs={"class": "fb_checkbox_field"}),
    ),
    "organization": forms.ModelChoiceField(
        label="The organization (Club or Promoter) which will be listed as the event host",
        required=False,
        queryset=Organization.objects.filter(name="Bicycle Colorado"),
        widget=Select(attrs={"class": "fb_select_multiple", "placeholder": "Select an Organization"}),
    ),
}

event_fields_base = [
    "name",
    "website",
    "blurb",
    "start_date",
    "end_date",
    "city",
    "state",
    "tags",
]
event_fields_authenticated = event_fields_base + [
    "email",
    "logo",
    "description",
    "registration_website",
    "is_permitted",
    "permit_no",
]

event_fields_orgadmin = event_fields_authenticated + [
    "featured_event",
    "organization",
    "publish_type",
    "hero",
]

event_fields_staff = event_fields_orgadmin + ["approved"]


class EventCommunityForm(forms.ModelForm):
    turnstile = event_fields["turnstile"]
    user_first = event_fields["user_first"]
    user_last = event_fields["user_last"]
    user_email = event_fields["user_email"]
    name = event_fields["name"]
    tags = event_fields["tags"]
    blurb = event_fields["blurb"]
    website = event_fields["website"]
    city = event_fields["city"]
    start_date = event_fields["start_date"]
    end_date = event_fields["end_date"]
    state = event_fields["state"]

    class Meta:
        model = Event
        fields = event_fields_base


class EventAuthenticatedUserForm(forms.ModelForm):
    name = event_fields["name"]
    email = event_fields["email"]
    website = event_fields["website"]
    registration_website = event_fields["registration_website"]
    tags = event_fields["tags"]
    blurb = event_fields["blurb"]
    description = event_fields["description"]
    start_date = event_fields["start_date"]
    end_date = event_fields["end_date"]
    logo = event_fields["logo"]
    city = event_fields["city"]
    state = event_fields["state"]
    location = forms.CharField(widget=GoogleMapsWidget(), required=False)
    is_permitted = event_fields["is_permitted"]
    permit_no = event_fields["permit_no"]

    def clean(self):
        cleaned_data = super().clean()
        lat = self.data.get("location_lat")
        lon = self.data.get("location_lon")
        if lat and lon:
            cleaned_data["location_lat"] = lat
            cleaned_data["location_lon"] = lon
        return cleaned_data

    def save(self, commit=True):
        instance = super(EventAuthenticatedUserForm, self).save(commit=False)
        instance.location_lat = self.cleaned_data.get("location_lat")
        instance.location_lon = self.cleaned_data.get("location_lon")
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Event
        fields = event_fields_authenticated


class EventOrgAdminForm(forms.ModelForm):
    name = event_fields["name"]
    email = event_fields["email"]
    website = event_fields["website"]
    registration_website = event_fields["registration_website"]
    tags = event_fields["tags"]
    blurb = event_fields["blurb"]
    description = event_fields["description"]
    start_date = event_fields["start_date"]
    end_date = event_fields["end_date"]
    logo = event_fields["logo"]
    hero = event_fields["hero"]
    city = event_fields["city"]
    state = event_fields["state"]
    location = forms.CharField(widget=GoogleMapsWidget(), required=False)
    publish_type = event_fields["publish_type"]
    featured_event = event_fields["featured_event"]
    is_permitted = event_fields["is_permitted"]
    permit_no = event_fields["permit_no"]
    # We add the queryset in the view
    organization = event_fields["organization"]

    def clean(self):
        cleaned_data = super().clean()
        lat = self.data.get("location_lat")
        lon = self.data.get("location_lon")
        if lat and lon:
            cleaned_data["location_lat"] = lat
            cleaned_data["location_lon"] = lon
        return cleaned_data

    def save(self, commit=True):
        instance = super(EventOrgAdminForm, self).save(commit=False)
        instance.location_lat = self.cleaned_data.get("location_lat")
        instance.location_lon = self.cleaned_data.get("location_lon")
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Event
        fields = event_fields_orgadmin


class EventStaffForm(forms.ModelForm):
    name = event_fields["name"]
    website = event_fields["website"]
    registration_website = event_fields["registration_website"]
    email = event_fields["email"]
    featured_event = event_fields["featured_event"]
    is_permitted = event_fields["is_permitted"]
    permit_no = event_fields["permit_no"]
    tags = event_fields["tags"]
    logo = event_fields["logo"]
    hero = event_fields["hero"]
    blurb = event_fields["blurb"]
    description = event_fields["description"]
    start_date = event_fields["start_date"]
    end_date = event_fields["end_date"]
    city = event_fields["city"]
    state = event_fields["state"]
    location = forms.CharField(widget=GoogleMapsWidget(), required=False)
    publish_type = event_fields["publish_type"]
    # We add the queryset in the view
    organization = event_fields["organization"]
    approved = event_fields["approved"]

    def clean(self):
        cleaned_data = super().clean()
        lat = self.data.get("location_lat")
        lon = self.data.get("location_lon")
        if lat and lon:
            cleaned_data["location_lat"] = lat
            cleaned_data["location_lon"] = lon
        return cleaned_data

    def save(self, commit=True):
        instance = super(EventStaffForm, self).save(commit=False)
        instance.location_lat = self.cleaned_data.get("location_lat")
        instance.location_lon = self.cleaned_data.get("location_lon")
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Event
        fields = event_fields_staff


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"


class RaceSeriesForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, queryset=Event.objects.all().order_by("name")
    )
    organization = forms.ModelChoiceField(Organization.objects.all().order_by("name"))

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
        labels = {"organization": "Hosting Organization", "name": "Race Series Name, include year in the name."}

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
