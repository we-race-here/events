from django import forms
from django.forms.widgets import TextInput, Textarea, Select, FileInput, CheckboxInput
from phonenumber_field.formfields import PhoneNumberField

from apps.membership.models import Organization, OrganizationMember

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


class OrganizationForm(forms.ModelForm):
    name = forms.CharField(
        label="Club Name",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Name of the Club",
                "max_length": 75,
            }
        ),
    )
    website = forms.URLField(
        label="Club website or other URL. Include https://...",
        required=False,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Website, Facebook, or other URL",
                "max_length": 100,
            }
        ),
    )
    phone = PhoneNumberField(
        label="Phone number (555) 555-5555",
        required=False,
        region="US",
        widget=forms.TextInput(attrs={"class": "fb_text_input_field", "placeholder": "(555) 555-5555"}),
    )
    email = forms.EmailField(
        label="Club Contact Email Address",
        required=False,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "emails address",
                "max_length": 75,
            }
        ),
    )
    address = forms.CharField(
        label="Address (not public, for internal use only)",
        required=False,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Name of the event",
                "max_length": 75,
            }
        ),
    )
    city = forms.CharField(
        label="City",
        required=True,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "City",
                "max_length": 75,
            }
        ),
    )
    state = forms.ChoiceField(
        initial="CO",
        label="State",
        required=True,
        choices=STATE_CHOICES,
        widget=Select(attrs={"class": "fb_select_multiple", "placeholder": "State"}),
    )
    zipcode = forms.CharField(
        label="Zipcode",
        required=False,
        max_length=75,
        widget=TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "Zipcode",
                "max_length": 10,
            }
        ),
    )
    logo = forms.CharField(
        label="Club logo",
        required=False,
        widget=FileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer "
                "focus:outline-none"
            }
        ),
    )
    hero = forms.CharField(
        label="Club banner image",
        required=False,
        widget=FileInput(
            attrs={
                "class": "w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 cursor-pointer "
                "focus:outline-none"
            }
        ),
    )
    blurb = forms.CharField(
        label="Short Description",
        required=True,
        widget=Textarea(
            attrs={
                "class": "fb_text_area_field",
                "placeholder": "short description of the Club (250 characters max)",
                "rows": 3,
                "max_length": 250,
            },
        ),
    )
    description = forms.CharField(
        label="Description of the club",
        required=False,
        max_length=2500,
        widget=forms.Textarea(
            attrs={
                "class": "fb_text_area_field",
                "rows": 10,
                "placeholder": "Description of the club",
            }
        ),
    )
    waiver_text = forms.CharField(
        label="Waiver text or other test you want members to agree to when they join.",
        required=False,
        max_length=2500,
        widget=forms.Textarea(
            attrs={
                "class": "fb_text_area_field",
                "rows": 10,
                "placeholder": "New member agreement text",
            }
        ),
    )
    membership_open = forms.BooleanField(
        required=False,
        label="Allow members to join your organization.",
        initial=False,
        widget=CheckboxInput(attrs={"class": "fb_checkbox_field"}),
    )

    class Meta:
        model = Organization
        fields = [
            "name",
            "website",
            "phone",
            "email",
            "address",
            "city",
            "state",
            "zipcode",
            "logo",
            "hero",
            "blurb",
            "description",
            "waiver_text",
            "membership_open",
        ]


class OrganizationMemberJoinForm(forms.ModelForm):
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "border border-gray-300 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 text-gray-600 rounded-md p-2 w-full"
            }
        ),
    )

    class Meta:
        model = OrganizationMember
        fields = ["organization"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        self.organization = kwargs.pop("organization", None)
        super().__init__(*args, **kwargs)
        if self.organization:
            self.fields["organization"].initial = self.organization
            self.fields["organization"].queryset = Organization.objects.filter(pk=self.organization.pk)

    def save(self, commit=True):
        organization_member = super().save(commit=False)
        organization_member.user = self.user
        if commit:
            organization_member.save()
        return organization_member
