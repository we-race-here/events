from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from membership.models import Organization, Member

User = get_user_model()


def event_logo_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path
    return get_random_upload_path(str(Path('uploads', 'cycling_org', 'event', 'logo')), filename)


def event_attachment_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path
    return get_random_upload_path(str(Path('uploads', 'cycling_org', 'event_attachment')), filename)


class Event(models.Model):
    """
    Name: This is the event name. Migration, no change
    Description: This is a short un formated text about the event. Migration, no change
    Start_date: date and time. Migration, no change
    End_date: date and time.   Migration, no change
    organizer_email: Migration, no change
    country: defaults to usa. Migration, no change
    city: city, nearestm of the event. Migration, no change
    state: state of the event. Migration, no change
    Website: Event website, facebook page.... Migration, no change
    registration_website: Where a user would register for the event.
    logo: Small image, logo for the event.
    Tags: List of event types
    more_data: Json data: Contains,
    - panels: list of panels, like youtube or maps
    organization: the org that "ownes" the event
    source: ?
    prefs: Json field
    - banner_image: The image to use as the banner
    - information_board_content: The content to show on the information board
    approved: Has a BC admin approved the event for public viewing.
    """
    PUBLISH_TYPE_PUBLIC = 'public'
    PUBLISH_TYPE_ORG_PUBLIC = 'org_public'
    PUBLISH_TYPE_ORG_PRIVATE = 'org_private'
    PUBLISH_TYPE_CHOICES = (
        (PUBLISH_TYPE_PUBLIC, 'Public'),
        (PUBLISH_TYPE_ORG_PUBLIC, 'Org Public'),
        (PUBLISH_TYPE_ORG_PRIVATE, 'Org Private'),
    )
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    organizer_email = models.EmailField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    registration_website = models.URLField(max_length=500, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=event_logo_file_path_func)
    # hero = models.ImageField(null=True, blank=True, upload_to=event_hero_file_path_func)
    tags = ArrayField(
        models.CharField(max_length=100, blank=True),
        size=50,
        null=True,
        blank=True
    )
    more_data = models.JSONField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='events')
    source = models.CharField(max_length=16, null=True, editable=False)
    prefs = models.JSONField(null=True, blank=True, editable=False)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)
    permit_no = models.CharField(max_length=25, blank=True, null=True)
    is_usac_permitted = models.BooleanField(default=False)
    featured_event = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, null=True)
    publish_type = models.CharField(max_length=32, choices=PUBLISH_TYPE_CHOICES, null=True)
    shared_org_perms = models.JSONField(null=True, blank=True, editable=False)  # {org_id: 'view|edit'}
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.organizer_email:
            self.organizer_email = self.organizer_email.lower()
        if (self.organization or self.organization_id) and (self.publish_type is None):
            self.publish_type = self.PUBLISH_TYPE_ORG_PUBLIC
        if not self.publish_type:
            self.publish_type = self.PUBLISH_TYPE_PUBLIC
        if self.end_date and (self.end_date < self.start_date):
            raise ValidationError({'end_date': 'end_date should be greater than start_date'})
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventAttachment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to=event_attachment_file_path_func)
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256, null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    upload_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.file_name = self.file.name
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.file_name


class Race(models.Model):
    name = models.CharField(max_length=256)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='races')
    start_datetime = models.DateTimeField(null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name='races')
    more_data = models.JSONField(null=True, blank=True)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('name', 'event', 'organization'),)

    def __str__(self):
        return self.name


class RaceResult(models.Model):
    FINISH_STATUS_OK = 'ok'
    FINISH_STATUS_DNS = 'dns'
    FINISH_STATUS_DNF = 'dnf'
    FINISH_STATUS_CHOICES = (
        (FINISH_STATUS_OK, 'OK'),
        (FINISH_STATUS_DNS, 'DNS'),
        (FINISH_STATUS_DNF, 'DNF'),
    )

    rider = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, related_name='race_results')
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    place = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    finish_status = models.CharField(max_length=16, default=FINISH_STATUS_OK, choices=FINISH_STATUS_CHOICES)
    category = models.CharField(max_length=32, null=True, blank=False)
    more_data = models.JSONField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('rider', 'race', 'organization'),)

    def save(self, *args, **kwargs):
        if not self.more_data:
            self.more_data = {}
        if self.finish_status != self.FINISH_STATUS_OK:
            self.place = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.place}-{self.rider}'


# TODO: consider removing this.
class Category(models.Model):
    title = models.CharField(max_length=256, unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='categories')
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = (('title', 'organization'),)

    def __str__(self):
        return self.title


class RaceSeries(models.Model):
    name = models.CharField(max_length=256)
    events = models.ManyToManyField(Event, related_name='race_series')
    races = models.ManyToManyField(Race, related_name='race_series')
    # TODO: use a json field to define categories for a race series
    # categories = models.JSONField(null=True, blank=False)
    categories = models.ManyToManyField(Category, related_name='race_series')
    points_map = models.JSONField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='race_series')
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('name', 'organization'),)

    def __str__(self):
        return self.name


class RaceSeriesResult(models.Model):
    race_series = models.ForeignKey(RaceSeries, on_delete=models.CASCADE)
    race_result = models.ForeignKey(RaceResult, on_delete=models.CASCADE)
    # TODO: use json field in race series
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    place = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    more_data = models.JSONField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('race_series', 'race_result', 'category', 'organization'),)

    def save(self, *args, **kwargs):
        if not self.more_data:
            self.more_data = {}
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.category}-{self.place}'
