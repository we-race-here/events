"""
Not migrating
- class OrganizationMemberOrg(models.Model):
"""
from datetime import timedelta
from pathlib import Path

from cerberus import Validator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
# from jsonschema import Validator TODO: what is this?
from model_utils.tracker import FieldTracker
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

User = get_user_model()


def organization_logo_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path
    return get_random_upload_path(str(Path('uploads', 'cycling_org', 'organization', 'logo')), filename)


class OrganizationMember(models.Model):
    """
    organization: key to Organization the member record is for.
    member: key to Member the member record is for.
    is_admin: the Member is an admin of the Organization.
    is_master_admin: TODO: Remove this!
    membership_price: TODO: Remove this!
    membership_plan: TODO: Remove this!
    is_active: The member has a active/current membership, not expired. There is a background script that updates this
        from the expiration date. Admins are always active.
    org_member_uid: TODO: I dont think we need this.
    start_date: Join date, This is the date of first join.
    exp_date: Default is members are renewed evenry calendar year. Jan 1 - Dec 31
    # TODO: Remove member_fields
    member_fields: custom field the Org defiines for the member. This is a JSONField.
    # TODO: remove status. This was used when inviting members to join an organization.
    status = models.CharField(max_length=16, null=True, choices=STATUS_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)
    history: tacks changes to the record
    _tracker = FieldTracker()
    """
    # STATUS_ACCEPT = 'accept'
    # STATUS_REJECT = 'reject'
    # STATUS_WAITING = 'waiting'
    # STATUS_CHOICES = (
    #     (STATUS_ACCEPT, 'Accept'),
    #     (STATUS_REJECT, 'Reject'),
    #     (STATUS_WAITING, 'Waiting'),
    # )
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    # TODO: Migrate all is_master_admin to is_admin
    # is_master_admin = models.BooleanField(default=False)
    # TODO: Removing membership pricing for now, may reimplement later.
    # membership_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)  # TODO: Drop me!
    # membership_plan = models.JSONField(null=True, blank=True, editable=False)
    is_active = models.BooleanField(default=True, null=True)
    #  TODO: Remove org_member_uid
    # org_member_uid = models.CharField(max_length=256, null=True, blank=True)
    start_date = models.DateField(null=True)
    exp_date = models.DateField(null=True)
    # TODO: Remove member_fields
    # member_fields = models.JSONField(null=True, blank=True)
    # TODO: remove status. This was used when inviting members to join an organization.
    # status = models.CharField(max_length=16, null=True, choices=STATUS_CHOICES)
    datetime = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()
    _tracker = FieldTracker()  # TODO: do we need this?

    class Meta:
        unique_together = [['organization', 'member']]

    # def jsonify_entry_form(self):
    #     for f in (self.organization.member_fields_schema or []):
    #         name = f['name']
    #         value = self.member_fields.get(name)
    #         if not value:
    #             continue
    #         if f['type'] == 'time':
    #             self.member_fields[name] = value.strftime('%H:%M:%S')
    #         elif f['type'] == 'date':
    #             self.member_fields[name] = value.strftime('%Y-%m-%d')
    #         elif f['type'] == 'datetime':
    #             self.member_fields[name] = value.isoformat()

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
        # TODO: Remove unused fields
        # if not self.org_member_uid:
        #     self.org_member_uid = None
        # if self.is_master_admin:
        #     self.is_admin = True
        # if self.member_fields and not kwargs.pop('_ignore_member_fields', False):
        #     v = Validator(self.organization.normalized_member_fields_schema, allow_unknown=True)
        #     if not v.validate(self.member_fields or {}):
        #         raise ValidationError({'member_fields': str(v.errors)})
        #     self.member_fields = v.document
        #     self.jsonify_entry_form()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.organization} - {self.member} - {self.is_admin} - {self.is_active} - {self.start_date} - {self.exp_date}'


# @FieldsTracking.register() TODO: do we need this?
class Organization(models.Model):
    """
    name: Name of the organization
    type: Regional, Club, Promoter, advocacy_volunteer. This effects some views.
    social_media: Social media links
    website: URL to the website, facebook, ...
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    phone_verified: Verify so that we can send sms messages.
    email: Email address
    email_verified: We don't need to implement verification now.
    address: Street address
    country: Country, default USA
    city: City
    state: State default Colorado
    zipcode: Zipcode
    about: Short unformated text.
    details: Long formated text. TODO: New field, form prefs.information_board_content
    logo: Small image
    hero: larger banner, hero image TODO: New field, form prefs.banner_image
    signup_config: TODO: remove this
    membership_plans: TODO: remove this
    member_fields_schema: TODO: remove this
    verified = models.BooleanField(default=False)
    prefs = models.JSONField(null=True, blank=True, editable=True)
    - banner_image: TODO: Move to hero
    - information_board_content: TODO: move to details
    members = models.ManyToManyField('Member', related_name='organizations', through=OrganizationMember)
    member_orgs: TODO: remove this, do not implement now.
    membership_open: True, False, if allowing new members
    approved: New orgs must be approved by BC is_staff
    rss_url: TODO: remove this
    waiver_text: This is shown on the join org page and useer must agree to it.
    _tracker: TODO, do we need this?
    """
    # TODO: No custom pricing membership fields or plans.
    # PERIODS_DAYS = {'1week': 7, '1month': 30, '3month': 120, '6month': 180, '1year': 365, '2year': 730}
    # MEMBER_FIELDS_SCHEMA_VALIDATOR = {
    #     'type': 'list', 'empty': True, 'required': False,
    #     'schema': {
    #         'type': 'dict', 'schema': {
    #             'name': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    #             'title': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    #             'type': {
    #                 'type': 'string', 'required': True, 'nullable': False, 'empty': False,
    #                 'allowed': [
    #                     'integer', 'float', 'number', 'string', 'text', 'boolean', 'percent', 'date', 'time', 'datetime'
    #                 ]
    #             },
    #             'required': {'type': 'boolean', 'required': False, 'default': False},
    #             'private': {'type': 'boolean', 'required': False, 'default': False},
    #             'choices': {
    #                 'type': 'list', 'required': False, 'nullable': True, 'empty': True,
    #                 'schema': {
    #                     'type': 'dict', 'empty': False,
    #                     'schema': {'title': {'type': 'string'}, 'value': {}}
    #                 }
    #             },
    #             'multiple': {'type': 'boolean', 'required': False, 'default': False},
    #         }
    #     },
    # }
    #
    # MEMBERSHIP_PLAN_SCHEMA_VALIDATOR = {
    #     'type': 'list', 'empty': True, 'required': False,
    #     'schema': {
    #         'type': 'dict', 'schema': {
    #             'id': {'type': 'string', 'required': True, 'nullable': False, 'empty': False},
    #             'title': {'type': 'string', 'required': False, 'nullable': True, 'empty': True},
    #             'period': {
    #                 'type': 'string', 'required': True, 'nullable': False, 'empty': False,
    #                 'allowed': ['1week', '1month', '3month', '6month', '1year', '2year']
    #             },
    #             'price': {
    #                 'type': 'decimal', 'required': True, 'nullable': False, 'empty': False, 'coerce': decimal.Decimal
    #             },
    #         }
    #     },
    # }

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
    phone_verified = models.BooleanField(default=None, null=True)
    email = models.EmailField(null=True, blank=True)
    email_verified = models.BooleanField(default=None, null=True)
    address = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=organization_logo_file_path_func)
    # hero = models.ImageField(null=True, blank=True, upload_to=organization_hero_file_path_func)
    signup_config = models.JSONField(null=True, blank=True)
    membership_plans = models.JSONField(null=True, blank=True)
    member_fields_schema = models.JSONField(null=True, blank=True)
    # TODO: remove I dont know what this is for
    verified = models.BooleanField(default=False)
    # TODO: banner_image and Info board are moved out. Is there anything else here?
    # prefs = models.JSONField(null=True, blank=True, editable=True)
    members = models.ManyToManyField('Member', related_name='organizations', through=OrganizationMember)
    # member_orgs = models.ManyToManyField('Organization', related_name='organizations', through=OrganizationMemberOrg)
    membership_open = models.BooleanField(default=False, null=True, blank=True)
    approved = models.BooleanField(default=False, null=True)  # New orgs must be approved by BC staff
    # TODO: remove RSS feed
    rss_url = models.TextField(default=None, null=True, blank=True)
    waiver_text = models.TextField(default=None, null=True, blank=True)
    _tracker = FieldTracker()

    # @property
    # def normalized_member_fields_schema(self): TODO: remove
    #     from events.helpers import (date_coerce, time_coerce, datetime_coerce, float_safe_coerce,
    #                                 number_safe_coerce, integer_safe_coerce)
    #     coerces = {
    #         'integer': integer_safe_coerce,
    #         'float': float_safe_coerce,
    #         'number': number_safe_coerce,
    #         'date': date_coerce,
    #         'time': time_coerce,
    #         'datetime': datetime_coerce,
    #     }
    #     schema = {}
    #     for f in (self.member_fields_schema or []):
    #         d = dict(type=f.get('type'))
    #
    #         # type
    #         if d['type'] == 'percent':
    #             d['type'] = 'integer'
    #             d['min'] = 0
    #             d['max'] = 100
    #         elif d['type'] == 'text':
    #             d['type'] = 'string'
    #         if d['type'] in coerces:
    #             d['coerce'] = coerces[d['type']]
    #
    #         # required
    #         required = f.get('required') is True
    #         d['required'] = required
    #         d['nullable'] = not required
    #         d['empty'] = not required
    #
    #         # choices
    #         choices = f.get('choices')
    #         if choices:
    #             d['allowed'] = [c.get('value') for c in choices]
    #         if f.get('multiple'):
    #             schema[f['name']] = {
    #                 'type': 'list', 'schema': d, 'required': required, 'nullable': not required, 'empty': not required
    #             }
    #         else:
    #             schema[f['name']] = d
    #
    #     return schema

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()

        # if self.member_fields_schema: TODO: remove
        #     v = Validator({'member_fields_schema': self.MEMBER_FIELDS_SCHEMA_VALIDATOR}, purge_unknown=True)
        #     if not v.validate({'member_fields_schema': self.member_fields_schema}):
        #         raise ValidationError({'member_fields_schema': str(v.errors)})
        #     self.member_fields_schema = v.document['member_fields_schema']
        # else:
        #     self.member_fields_schema = []

        if self.social_media:
            v = Validator(self.SOCIAL_MEDIA_SCHEMA, allow_unknown=True)
            if not v.validate(self.social_media):
                raise ValidationError({'social_media': str(v.errors)})
            self.social_media = v.document
        else:
            self.social_media = {}

        # if self.membership_plans: TODO: remove
        #     v = Validator({'membership_plans': self.MEMBERSHIP_PLAN_SCHEMA_VALIDATOR}, allow_unknown=True)
        #     if not v.validate({'membership_plans': self.membership_plans}):
        #         raise ValidationError({'membership_plans': str(v.errors)})
        #     self.membership_plans = v.document['membership_plans']
        # else:
        #     self.membership_plans = []

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'


class Member(models.Model):
    """
    first_name:
    last_name:
    gender: see options
    birth_date:
    phone:
    phone_verified: Verify so we can send sms
    email:
    email_verified: Required to on new account to login.
    address1:
    address2:
    country:
    city:
    state:
    zipcode:
    weight: save value in KG
    height: save value in CM
    social_media = models.JSONField(null=True, blank=True)
    TODO: avitar user.avatar, we can reset this for migration.
    TODO: I dont think we have anything in more data.
    more_data = models.JSONField(null=True, blank=True)
    TODO: Remove is_verified: I think this is related to verified email or sms. it could be a @property
    is_verified = models.BooleanField(default=None, null=True)
    TODO: Remove Draft. this was the status before a email or sms was verified, remove
    draft = models.BooleanField(default=False, null=False, editable=False)
    TODO: rename: usac_license_number to usac_license
    usac_license_number = models.IntegerField(null=True, blank=True, unique=True)
    TODO: rename: usac_license_number_verified to usac_license_verified
    usac_license_number_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='member', null=True, blank=True)
    """
    SOCIAL_MEDIA_SCHEMA = {
        'zwift': {
            'type': 'string', 'required': False, 'nullable': True, 'meta': {'title': 'Zwift'}
        },
        'zwiftpower': {
            'type': 'string', 'required': False, 'nullable': True, 'meta': {'title': 'Zwift Power'}
        },
        'strava': {
            'type': 'string', 'required': False, 'nullable': True, 'meta': {'title': 'Strava'}
        },
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

    USER_SHARED_FIELDS = ('first_name', 'last_name', 'birth_date', 'gender')

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'
    GENDER_UNKNOWN = 'u'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male'),
        (GENDER_FEMALE, 'Female'),
        (GENDER_OTHER, 'Other'),
        (GENDER_UNKNOWN, 'Unknown'),
    )
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    birth_date = models.DateField(null=True, blank=True)
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    phone_verified = models.BooleanField(default=None, null=True)
    email = models.EmailField(null=True, blank=True)
    email_verified = models.BooleanField(default=None, null=True)
    address1 = models.CharField(max_length=256, blank=True, null=True)
    address2 = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    weight = models.DecimalField('Weight (kg)', max_digits=5, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(10), MaxValueValidator(300)])
    height = models.DecimalField('Height (m)', max_digits=3, decimal_places=2, null=True, blank=True,
                                 validators=[MinValueValidator(1), MaxValueValidator(3)])

    social_media = models.JSONField(null=True, blank=True)
    # TODO: Are we using more_data?
    # more_data = models.JSONField(null=True, blank=True)
    # TODO: need some way to mark a user has verified email (Draft oris_verified
    is_verified = models.BooleanField(default=None, null=True)
    # draft = models.BooleanField(default=False, null=False, editable=False)
    usac_license = models.IntegerField(null=True, blank=True, unique=True)
    usac_license_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name='member', null=True, blank=True)

    @property
    def age(self):
        if not self.birth_date:
            return
        return timezone.now().year - self.birth_date.year

    def generate_verify_code(self, type='email'):
        '''
        :param type: can be "email" or "phone"
        :return: str of numbers
        '''
        from events.helpers import get_member_verify_otp
        return get_member_verify_otp(self, salt=type).now()

    def check_verify_code(self, code, type='email', valid_window=0):
        '''
        :param code: str of numbers
        :param type: can be "email" or "phone"
        :return: True if verified else False
        '''
        from events.helpers import get_member_verify_otp
        return get_member_verify_otp(self, salt=type).verify(code, valid_window=valid_window)

    def save(self, *args, **kwargs):
        if not self.phone:
            self.phone = None
        if not self.email:
            self.email = None
        if not self.email_verified:
            self.email_verified = None
        if not self.phone_verified:
            self.phone_verified = None
        if not self.is_verified:
            self.is_verified = None
        if self.email:
            self.email = self.email.lower()
        if not self.usac_license_number:
            self.usac_license = None
            self.usac_license_verified = False

        if self.social_media:
            v = Validator(self.SOCIAL_MEDIA_SCHEMA, allow_unknown=True)
            if not v.validate(self.social_media):
                raise ValidationError({'social_media': str(v.errors)})
            self.social_media = v.document
        else:
            self.social_media = {}
        return super().save(*args, **kwargs)

    def set_as_verified(self, user, commit=True):
        self.email_verified = True
        self.is_verified = True
        self.draft = False
        self.user = user
        member_data = (user.more_data or {}).get('member_data') or {}
        fields = ('phone', 'address1', 'address2', 'country', 'city', 'state', 'zipcode', 'usac_license_number')
        member_data = {k: member_data.get(k) for k in fields}
        member_data.update(first_name=user.first_name, last_name=user.last_name, gender=user.gender,
                           birth_date=user.birth_date, user=user, email=user.email)
        for k, v in member_data.items():
            if k == 'gender' and v is not None:
                setattr(self, k, v)
            elif not getattr(self, k, None):
                setattr(self, k, v)

        if commit:
            self.save()

    class Meta:
        # TODO: what about user name? is it forced to email?
        unique_together = (('email', 'email_verified'), ('phone', 'phone_verified'),)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.email}'
