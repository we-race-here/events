import json
from datetime import date, datetime

from allauth.account.forms import LoginForm, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import BooleanField, CharField, CheckboxInput, ChoiceField, EmailField
from django.utils.translation import gettext_lazy as _
from turnstile.fields import TurnstileField

User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    DAY_CHOICES = [(None, "Select Day")] + [(day, day) for day in range(1, 32)]
    MONTH_CHOICES = [(None, "Select Month")] + [(month, month) for month in range(1, 13)]
    YEAR_CHOICES = [(None, "Select Year")] + [
        (year, year) for year in range(2023, 1899, -1)
    ]  # Adjust the range accordingly
    first_name = forms.CharField(max_length=30, label="First Name")
    last_name = forms.CharField(max_length=30, label="Last Name")
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    birth_day = forms.ChoiceField(
        choices=DAY_CHOICES, required=True, label="Birth Day", widget=forms.Select(attrs={"id": "id_birth_day"})
    )
    birth_month = forms.ChoiceField(
        choices=MONTH_CHOICES, required=True, label="Birth Month", widget=forms.Select(attrs={"id": "id_birth_month"})
    )
    birth_year = forms.ChoiceField(
        choices=YEAR_CHOICES, required=True, label="Birth Year", widget=forms.Select(attrs={"id": "id_birth_year"})
    )

    gender = ChoiceField(choices=[("", "Select Gender"), ("M", "Male"), ("F", "Female"), ("O", "Other")], required=True)
    usac_number = CharField(required=False, label="USAC Number", empty_value=None)
    opt_in_email = BooleanField(widget=CheckboxInput(), label="Opt out of promotional emails", required=False)
    terms_of_service = BooleanField(required=True, widget=CheckboxInput(), label="I agree to Terms and Service")
    privacy_policy = BooleanField(required=True, widget=CheckboxInput(), label="I agree to Privacy Policy")
    user_agreement_waiver = BooleanField(required=True, widget=CheckboxInput(), label="I accept the waiver")
    parent_user_agreement_waiver = BooleanField(required=False, widget=CheckboxInput(), label="I accept the waiver")
    parent_terms_of_service = BooleanField(required=False, widget=CheckboxInput(), label="I agree to Terms and Service")

    turnstile = TurnstileField(label="")

    parent_name = forms.CharField(required=False)
    parent_email = forms.EmailField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        birth_day = cleaned_data.get("birth_day")
        birth_month = cleaned_data.get("birth_month")
        birth_year = cleaned_data.get("birth_year")
        parent_name = cleaned_data.get("parent_name")
        parent_email = cleaned_data.get("parent_email")

        # Create a date object from the birth day, month, and year
        dob = date(int(birth_year), int(birth_month), int(birth_day))

        # Calculate the user's age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Check the age and the presence of parent's details
        if age < 18:
            if not parent_name or not parent_email:
                raise forms.ValidationError("Parent's name and email are required for users under 18.")

        return cleaned_data

    def save(self, request):
        user = super().save(request)

        try:
            # Create a dictionary from form data excluding password
            form_data = {key: value for key, value in self.cleaned_data.items() if key != "password"}

            # Adding request metadata to the dictionary
            def is_jsonable(x):
                try:
                    json.dumps(x)
                    return True
                except (TypeError, OverflowError):
                    return False

            request_meta_data = {k: v for k, v in request.META.items() if is_jsonable(v)}

            form_data.update(
                {
                    "META": request_meta_data,
                }
            )
            form_data["timestamp"] = datetime.now().isoformat()  # Current date & time

            # Save the dictionary in the user_agreement_waiver_record field
            user.user_agreement_waiver_record = json.dumps(form_data)
            user.save()
        except Exception as e:
            print("Exception", str(e))

        # User is a minor, send email to the parent
        # if 13 <= user.age < 18:
        #     send_parent_email(user)

        return user


class UserLoginForm(LoginForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """

    turnstile = TurnstileField(label="")


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
