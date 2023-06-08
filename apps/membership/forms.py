from django import forms

from apps.membership.models import Organization, OrganizationMember


class OrganizationForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "ckeditor"}))

    class Meta:
        model = Organization
        fields = [
            "name",
            "type",
            "blurb",
            "description",
            "website",
            "phone",
            "email",
            "address",
            "country",
            "city",
            "state",
            "zipcode",
            "logo",
            "hero",
            "waiver_text",
            "membership_open",
        ]
        labels = {
            "hero": "Add a hero image to your profile",
            "waiver_text": "Add waiver text if you want members to agree to a waiver when they join.",
            "membership_open": "Allow members to join your organization.",
        }
        css = (
            "block py-2.5 px-0 bg-white text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 "
            "appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none "
            "focus:ring-0 focus:border-blue-600 peer"
        )
        waiver_css = (
            "block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 "
            "focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 "
            "dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        )

        widgets = {
            "name": forms.TextInput(attrs={"class": css}),
            "blurb": forms.Textarea(attrs={"rows": 5, "class": css + " w-full"}),
            "type": forms.Select(
                attrs={
                    "class": '"block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 '
                    "border-gray-300 appearance-none dark:text-white dark:border-gray-600 "
                    'dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"'
                }
            ),
            "website": forms.TextInput(attrs={"class": css}),
            "phone": forms.TextInput(attrs={"class": css}),
            "email": forms.TextInput(attrs={"class": css}),
            "address": forms.TextInput(attrs={"class": css}),
            "country": forms.TextInput(attrs={"class": css}),
            "city": forms.TextInput(attrs={"class": css}),
            "state": forms.TextInput(attrs={"class": css}),
            "zipcode": forms.TextInput(attrs={"class": css}),
            "logo": forms.ClearableFileInput(attrs={"class": "border rounded-lg px-3 py-2 w-full"}),
            "hero": forms.ClearableFileInput(attrs={"class": "border rounded-lg px-3 py-2 w-full"}),
            "waiver_text": forms.Textarea(
                attrs={
                    "rows": "5",
                    "class": waiver_css,
                }
            ),
            "membership_open": forms.CheckboxInput(attrs={"class": "border rounded-lg px-3 py-2"}),
        }


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
