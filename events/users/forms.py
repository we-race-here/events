import json
from datetime import date, datetime

from allauth.account.forms import LoginForm, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import BooleanField, CharField, CheckboxInput, ChoiceField, EmailField, TextInput, PasswordInput
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


def widget_attrs(class_name, grid_size=None, placeholder=None):
    """Helper function to return common widget attributes."""
    attrs = {"class": class_name}
    if grid_size:
        attrs["grid_size"] = grid_size
    if placeholder:
        attrs["placeholder"] = placeholder
    return attrs


class UserSignupForm(SignupForm):
    """Form for user sign-up."""

    # Birth Date Fields
    DAY_CHOICES = [(None, "Select Day")] + [(day, day) for day in range(1, 32)]
    MONTH_CHOICES = [(None, "Select Month")] + [(month, month) for month in range(1, 13)]
    YEAR_CHOICES = [(None, "Select Year")] + [(year, year) for year in range(2023, 1899, -1)]

    birth_day = forms.ChoiceField(choices=DAY_CHOICES,
                                  widget=forms.Select(attrs=widget_attrs("fb_select_multiple", "w-1/3")))
    birth_month = forms.ChoiceField(choices=MONTH_CHOICES,
                                    widget=forms.Select(attrs=widget_attrs("fb_select_multiple", "w-1/3")))
    birth_year = forms.ChoiceField(choices=YEAR_CHOICES,
                                   widget=forms.Select(attrs=widget_attrs("fb_select_multiple", "w-1/3")))

    # User Information Fields
    first_name = forms.CharField(widget=forms.TextInput(attrs=widget_attrs("fb_select_multiple", "w-1/2")))
    last_name = forms.CharField(widget=forms.TextInput(attrs=widget_attrs("fb_select_multiple", "w-1/2")))
    gender = forms.ChoiceField(choices=[("", "Select Gender"), ("M", "Male"), ("F", "Female"), ("O", "Other")],
                               widget=forms.Select(attrs=widget_attrs("fb_select_multiple", "w-1/2")))
    usac_number = forms.CharField(required=False,
                                  widget=forms.TextInput(attrs=widget_attrs("fb_select_multiple", "w-1/2")))

    # Agreement Fields
    opt_in_email = forms.BooleanField(widget=forms.CheckboxInput(), required=False,
                                      label="Opt out of promotional emails")
    terms_of_service = forms.BooleanField(widget=forms.CheckboxInput(), label="I agree to Terms and Service")
    privacy_policy = forms.BooleanField(widget=forms.CheckboxInput(), label="I agree to Privacy Policy")
    user_agreement_waiver = forms.BooleanField(widget=forms.CheckboxInput(), label="I accept the waiver")

    # Metadata
    class Meta:
        fields = []

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

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
    def __init__(self, *args, **kwargs):
        super(UserSignupForm, self).__init__(*args, **kwargs)
        # Modify the email field's widget
        self.fields['email'].widget = TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "E-mail",
                "max_length": 20,
            }
        )




class UserLoginForm(LoginForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """
    # turnstile = TurnstileField(label="")


    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        # Modify the email field's widget
        self.fields['login'].widget = TextInput(
            attrs={
                "class": "fb_text_input_field",
                "placeholder": "E-mail",
                "max_length": 20,
            }
        )

        # Add class to password field's widget
        self.fields['password'].widget.attrs.update({
            "class": "fb_text_input_field",
        })



class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
