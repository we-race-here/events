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
from django.forms.widgets import Textarea, SelectDateWidget, ClearableFileInput
from django.utils.datetime_safe import datetime
from turnstile.fields import TurnstileField

from apps.membership.models import Organization
from .models import Event, Race, RaceResult, RaceSeries, event_types

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


############################################################################################################
# Event Forms
############################################################################################################
event_fields = {
    "turnstile": TurnstileField(label=""),
    "description": forms.CharField(
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
    "logo": forms.CharField(
        widget=FileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400"
            }
        )
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
                "max_length": 50,
            }
        ),
    ),
    "tags": forms.MultipleChoiceField(
        label="Select Event Tag(s)",
        choices=event_types,
        widget=SelectMultiple(
            attrs={"class": "fb_select_multiple", "placeholder": "Event tags and type", "help_text": "select multiple"}
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
}

event_fields_base = [
    "name",
    "blurb",
    "start_date",
    "end_date",
    "website",
    "city",
    "state",
    "tags",
]
event_fields_authenticated = event_fields_base + ["logo", "description"]
event_labels_base = {
    "name": "Event Name",
    "blurb": "Event Blurb",
    "start_date": "Event Start Date",
    "end_date": "Event End Date",
    "website": "Event Website or other URL",
    "city": "Event City",
    "state": "Event State",
    "tags": "Event Tags",
}
event_labels_authenticated = event_labels_base.copy()
event_labels_authenticated.update(
    {
        "logo": "Event logo. Suggested size (250X250)",
        "description": "Event Description",
    }
)

event_widgets_base = {
    "name": TextInput(
        attrs={
            "class": "fb_text_input_field",
            "placeholder": "event name (50 characters max)",
            "max_length": 50,
        }
    ),
    "blurb": Textarea(
        attrs={
            "class": "fb_text_area_field",
            "placeholder": "short description of the event (250 characters max)",
            "rows": 4,
            "max_length": 50,
        },
    ),
    "website": TextInput(
        attrs={
            "class": "fb_text_input_field",
            "placeholder": "Website, Facebook, Instagram, etc.",
        }
    ),
    "event_city": TextInput(
        attrs={
            "class": "fb_text_input_field",
            "placeholder": "Nearest City",
            "max_length": 50,
        }
    ),
    "event_state": TextInput(
        attrs={
            "class": "fb_text_input_field",
            "placeholder": "event name (50 characters max)",
            "max_length": 50,
        }
    ),
}

event_widgets_authenticated = event_widgets_base.copy()
event_widgets_authenticated.update(
    {
        "logo": ClearableFileInput(),
        #         "description": TinyMCE(attrs={"cols": 80, "rows": 30}),
    }
)


class EventStaffForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        label="Select Event Tag(s)",
        choices=event_types,
        widget=SelectMultiple(
            attrs={"class": "fb_select_multiple", "placeholder": "Event tags and type", "help_text": "select multiple"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "A longer event description with basic formatting and links",
            }
        )
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "blurb",
            "description",
            "start_date",
            "end_date",
            "website",
            "city",
            "state",
            "tags",
        ]
        labels = {
            "name": "Event Name",
            "blurb": "Event Blurb",
            "description": "Event Description",
            "start_date": "Event Start Date",
            "end_date": "Event End Date",
            "website": "Event Website or other URL",
            "city": "Event City",
            "state": "Event State",
            "tags": "Event Tags",
        }
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "event name (50 characters max)",
                    "max_length": 50,
                }
            ),
            "blurb": Textarea(
                attrs={
                    "class": "fb_text_area_field",
                    "placeholder": "short description of the event (250 characters max)",
                    "rows": 4,
                    "max_length": 250,
                }
            ),
            "start_date": SelectDateWidget(
                attrs={"class": "fb_select_date_field"},
                years=range(datetime.now().year, datetime.now().year + 3),
            ),
            "end_date": SelectDateWidget(
                attrs={"class": "fb_select_date_field"},
                years=range(datetime.now().year, datetime.now().year + 3),
            ),
            "website": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "Website, Facebook, Instagram, etc.",
                }
            ),
            "event_city": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "Nearest City",
                    "max_length": 50,
                }
            ),
            "event_state": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "event name (50 characters max)",
                    "max_length": 50,
                }
            ),
        }


class EventCommunityForm(forms.ModelForm):
    turnstile = event_fields["turnstile"]
    user_first = event_fields["user_first"]
    user_last = event_fields["user_last"]
    user_email = event_fields["user_email"]
    tags = event_fields["tags"]
    start_date = event_fields["start_date"]
    end_date = event_fields["end_date"]

    class Meta:
        model = Event
        fields = event_fields_base
        labels = event_labels_base
        widgets = event_widgets_base


class EventAuthenticatedUserForm(forms.ModelForm):
    tags = event_fields["tags"]
    description = event_fields["description"]
    start_date = event_fields["start_date"]
    end_date = event_fields["end_date"]
    logo = event_fields["logo"]

    class Meta:
        model = Event
        fields = event_fields_authenticated
        labels = event_labels_authenticated
        widgets = event_widgets_authenticated


class EventOrgAdminForm(forms.ModelForm):
    tags = forms.MultipleChoiceField(
        label="Select Event Tag(s)",
        choices=event_types,
        widget=SelectMultiple(
            attrs={"class": "fb_select_multiple", "placeholder": "Event tags and type", "help_text": "select multiple"}
        ),
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "A longer event description with basic formatting and links",
            }
        )
    )

    class Meta:
        model = Event
        fields = [
            "name",
            "blurb",
            "description",
            "start_date",
            "end_date",
            "website",
            "city",
            "state",
            "tags",
        ]
        labels = {
            "name": "Event Name",
            "blurb": "Event Blurb",
            "description": "Event Description",
            "start_date": "Event Start Date",
            "end_date": "Event End Date",
            "website": "Event Website or other URL",
            "city": "Event City",
            "state": "Event State",
            "tags": "Event Tags",
        }
        widgets = {
            "name": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "event name (50 characters max)",
                    "max_length": 50,
                }
            ),
            "blurb": Textarea(
                attrs={
                    "class": "fb_text_area_field",
                    "placeholder": "short description of the event (250 characters max)",
                    "rows": 4,
                    "max_length": 250,
                }
            ),
            "start_date": SelectDateWidget(
                attrs={"class": "fb_select_date_field"},
                years=range(datetime.now().year, datetime.now().year + 3),
            ),
            "end_date": SelectDateWidget(
                attrs={"class": "fb_select_date_field"},
                years=range(datetime.now().year, datetime.now().year + 3),
            ),
            "website": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "Website, Facebook, Instagram, etc.",
                }
            ),
            "event_city": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "Nearest City",
                    "max_length": 50,
                }
            ),
            "event_state": TextInput(
                attrs={
                    "class": "fb_text_input_field",
                    "placeholder": "event name (50 characters max)",
                    "max_length": 50,
                }
            ),
        }


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
