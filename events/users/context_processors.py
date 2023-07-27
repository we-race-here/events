from django.conf import settings


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def version(context):
    """Expose the version of the application and alert to debug mode."""
    return {"DEBUG": settings.DEBUG}
