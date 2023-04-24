"""
Not migrating
- class OrganizationMemberOrg(models.Model):
"""
from datetime import timedelta
from pathlib import Path

from cerberus import Validator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
# from jsonschema import Validator TODO: what is this?
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

User = get_user_model()


def organization_logo_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path
    return get_random_upload_path(str(Path('uploads', 'cycling_org', 'organization', 'logo')), filename)


def organization_hero_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path
    return get_random_upload_path(str(Path('uploads', 'cycling_org', 'organization', 'hero')), filename)


class OrganizationMember(models.Model):
    """
    organization: key to Organization the member record is for.
    member: key to Member the member record is for.
    is_admin: the Member is an admin of the Organization.
    is_master_admin: TODO: Removed
    membership_price: TODO: Removed
    membership_plan: TODO: Removed
    is_active: The member has a active/current membership, not expired. There is a background script that updates this
        from the expiration date. Admins are always active.
    org_member_uid: TODO: I dont think we need this.
    start_date: Join date, This is the date of first join.
    exp_date: Default is members are renewed evenry calendar year. Jan 1 - Dec 31
    member_fields: custom field the Org defines for the member. This is a JSONField. TODO: Removed
    status = models.CharField(max_length=16, null=True, choices=STATUS_CHOICES) TODO: removed
    datetime = models.DateTimeField(auto_now_add=True)
    history: tacks changes to the record
    """
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, null=True)
    start_date = models.DateField(null=True)
    exp_date = models.DateField(null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = [['organization', 'user']]

    def is_expired(self):
        if not self.exp_date:
            return False
        return timezone.now().date() > self.exp_date

    def is_expiring(self, days=5):
        if not self.exp_date:
            return False
        return timezone.now().date() >= (self.exp_date - timedelta(days=days))

    def save(self, *args, **kwargs):
        if not self.is_active:
            self.is_active = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.organization} - {self.user} - {self.is_admin} - {self.is_active} - {self.start_date} - {self.exp_date}'


# @FieldsTracking.register() TODO: do we need this?
class Organization(models.Model):
    """
    name: Name of the organization
    type: Regional, Club, Promoter, advocacy_volunteer. This effects some views.
    social_media: Social media links
    website: URL to the website, facebook, ...
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    phone_verified: Verify so that we can send sms messages. TODO: Removed
    email: Email address
    email_verified: We don't need to implement verification now. TODO: removed
    address: Street address
    country: Country, default USA
    city: City
    state: State default Colorado
    zipcode: Zipcode
    about: Short unformated text.
    details: Long formated text. TODO: New field, form prefs.information_board_content
    logo: Small image
    hero: larger banner, hero image TODO: New field, form prefs.banner_image, dont need to migrate
    signup_config: TODO: removed
    membership_plans: TODO: removed
    member_fields_schema: TODO: removed
    verified = models.BooleanField(default=False) TODO: removed
    prefs = models.JSONField(null=True, blank=True, editable=True)
    - banner_image: TODO: Use hero, don't need to migrate, user can update later
    - information_board_content: TODO: move to details, Dont need to migrate, user can update later.
    user = models.ManyToManyField(User, related_name='organizations', through=OrganizationMember)
    member_orgs: TODO: removed
    membership_open: True, False, if allowing new members
    approved: New orgs must be approved by BC is_staff
    rss_url: TODO: removed
    waiver_text: This is shown on the join org page and useer must agree to it.
    _tracker: TODO, removed
    """
    SOCIAL_MEDIA_SCHEMA = {
        'youtube': {
            'type': 'string', 'required': False, 'nullable': True, 'meta': {'title': 'Youtube'}
        },
        'facebook': {
            'type': 'string', 'required': False, 'nullable': True, 'meta': {'title': 'Facebook'}
        },
        'instagram': {
            'type': 'string', 'required': False, 'nullable': True, 'meta': {'title': 'Instagram'}
        },
    }

    TYPE_REGIONAL = 'regional'
    TYPE_CLUB = 'club'
    TYPE_ADVOCACY_VOLUNTEER = 'advocacy_volunteer'
    TYPE_PROMOTER = 'promoter'
    TYPE_CHOICES = (
        (TYPE_REGIONAL, 'Regional'),
        (TYPE_CLUB, 'Club'),
        (TYPE_ADVOCACY_VOLUNTEER, 'Advocacy, Volunteer'),
        (TYPE_PROMOTER, 'Promoter'),
    )
    name = models.CharField(max_length=256, unique=True)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    social_media = models.JSONField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=organization_logo_file_path_func)
    hero = models.ImageField(null=True, blank=True, upload_to=organization_hero_file_path_func)
    user = models.ManyToManyField(User, related_name='organizations', through=OrganizationMember)
    membership_open = models.BooleanField(default=False, null=True, blank=True)
    approved = models.BooleanField(default=False, null=True)  # New orgs must be approved by BC staff
    waiver_text = models.TextField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        if self.social_media:
            v = Validator(self.SOCIAL_MEDIA_SCHEMA, allow_unknown=True)
            if not v.validate(self.social_media):
                raise ValidationError({'social_media': str(v.errors)})
            self.social_media = v.document
        else:
            self.social_media = {}
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
