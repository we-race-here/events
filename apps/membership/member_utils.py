import logging
from datetime import date
from itertools import chain

from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.membership.models import Organization, OrganizationMember
from apps.usac.models import UsacDownload

logger = logging.getLogger(__name__)

User = get_user_model()


def get_user(
    license: int = None,
    first_name: str = None,
    last_name: str = None,
    dob: str = None,
    email: str = None,
) -> User:
    """Try to find a matching user record"""
    if license:
        try:
            return User.objects.get(Q(license=license) & Q(license_verified=True))
        except User.DoesNotExist:
            pass
    elif email:
        try:
            return User.objects.get(Q(email=email) & Q(email_verified=True))
        except User.DoesNotExist:
            pass
    elif first_name and last_name and dob:
        try:
            return User.objects.get(Q(first_name__iexact=first_name) & Q(last_name__iexact=last_name) & Q(dob=dob))
        except User.DoesNotExist:
            pass
    else:
        return None


def get_usac_records(
    license: int = None,
    first_name: str = None,
    last_name: str = None,
    dob: str = None,
    email: str = None,
    user: User = None,
    club: str = None,
) -> dict:
    """Try to match usac records
    https://stackoverflow.com/questions/431628/how-to-combine-multiple-querysets-in-django
    """
    try:
        if not user:
            user = get_user(license, first_name, last_name, dob, email)
        if user:
            if user.usac_license_verified:
                by_usac_license = UsacDownload.objects.filter(
                    Q(usac_license=user.usac_license) & Q(expiration_date__exists=True)
                )
            by_user_name = UsacDownload.objects.filter(
                Q(first_name=user.first_name)
                & Q(last_name=user.last_name)
                & Q(date_of_birth=user.dob)
                & Q(expiration_date__exists=True)
            )
        by_name = UsacDownload.objects.filter(
            Q(first_name=first_name) & Q(last_name=last_name) & Q(date_of_birth=dob) & Q(expiration_date__exists=True)
        )
        by_name_club = UsacDownload.objects.filter(
            Q(first_name=first_name) & Q(last_name=last_name) & Q(club=club) & Q(expiration_date__exists=True)
        )
        usac_list = list(chain(by_usac_license, by_user_name, by_name, by_name_club))
        usac_dict = {
            "current": [l for l in usac_list if l.license_status == "Valid" and l.expiration_date >= date.today()]
        }
        usac_dict["other"] = [l for l in usac_list if l not in usac_dict["current"]]
    except Exception as e:
        logger.error(f"Error in get_usac_records: {e}")
        return None


def get_club(
    user: User = None,
    license: int = None,
    first_name: str = None,
    last_name: str = None,
    dob: str = None,
    email: str = None,
) -> dict:
    """Try to get the name of a club(s) for the person"""
    clubs = {}
    if not user:
        user = get_user(license, first_name, last_name, dob, email)
    if user:
        try:
            clubs["org_clubs"] = OrganizationMember.objects.filter(Q(user=user) & Q(type="club")).values_list(
                "organization__name", flat=True
            )
        except Exception:
            pass


def club_report():
    """Get a report of all clubs and their members
    USAC clubs for Current members
    system clubs for Current members
    """
    clubs = {}
    usac_query = Q(license_status="Valid") & Q(license_expiration__gte=date.today())
    clubs["usac_clubs"] = set(
        UsacDownload.objects.order_by("data__club").filter(usac_query).values_list("data__club", flat=True)
    )
    clubs["org_clubs"] = set(Organization.objects.order_by("name").filter(type="club").values_list("name", flat=True))
    clubs["both"] = clubs["usac_clubs"].intersection(clubs["org_clubs"])
    clubs["usac_only"] = clubs["usac_clubs"].difference(clubs["org_clubs"])
    clubs["org_only"] = clubs["org_clubs"].difference(clubs["usac_clubs"])
    return clubs


# org_clubs
