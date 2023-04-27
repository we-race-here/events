from typing import Any

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings
from django.http import HttpRequest


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.birth_date = form.cleaned_data.get("birth_date")
        user.gender = form.cleaned_data.get("gender")
        user.usac_number = form.cleaned_data.get("usac_number")
        user.opt_in_email = form.cleaned_data.get("opt_in_email")
        user.terms_of_service = form.cleaned_data.get("terms_of_service")
        user.user_agreement_waiver = form.cleaned_data.get("user_agreement_waiver")

        if commit:
            user.save()
        return user


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request: HttpRequest, sociallogin: Any):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)
