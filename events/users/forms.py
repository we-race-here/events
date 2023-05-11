from allauth.account.forms import LoginForm, SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.forms import BooleanField, CharField, CheckboxInput, ChoiceField, DateField, DateInput, EmailField
from django.forms.forms import Form
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

    birth_date = DateField(
        required=True,
        label="Date of Birth",
        widget=DateInput(
            attrs={
                "type": "date",
                "class": "appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 "
                "placeholder-gray-500 text-gray-900 rounded-t-md  rounded-b-md focus:outline-none "
                "focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
            }
        ),
    )
    gender = ChoiceField(
        choices=[("", "Select Gender"), ("M", "Male"), ("F", "Female"), ("O", "Other")], required=False
    )
    usac_number = CharField(required=False, label="USAC Number", empty_value=None)
    opt_in_email = BooleanField(widget=CheckboxInput(), label="Opt out of promotional emails", required=False)
    terms_of_service = BooleanField(required=True, widget=CheckboxInput(), label="I agree to Terms and Service")
    user_agreement_waiver = BooleanField(required=True, widget=CheckboxInput(), label="I accept the waiver")
    turnstile = TurnstileField(label="")


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
