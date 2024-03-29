import logging
from collections import defaultdict
from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models
from simple_history.models import HistoricalRecords

from apps.membership.models import Organization
from apps.usac.models import UsacDownload

logger = logging.getLogger(__name__)

User = get_user_model()

event_types = tuple(
    (t, t)
    for t in [
        "Road",
        "Criterium",
        "Cycle-Cross",
        "Mountain bike",
        "Hill Climb",
        "Time Trial",
        "Gran Fondo",
        "Tour",
        "BMX",
        "Cycling Camp",
        "Clinic",
        "Downhill",
        "Enduro",
        "Fat Bike",
        "Gravel",
        "Omnium",
        "Points Race",
        "Track",
        "Stage Race",
        "Team Time Trial",
        "Virtual",
        "Dual Slalom",
        "BC Road Cup",
        "BC Cycle-Cross Cup",
        "Collegiate Permitted",
        "BC State Championships",
        "Youth",
        "Fundraiser",
    ]
)


def event_logo_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path

    return get_random_upload_path(str(Path("uploads", "cycling_org", "event", "logo")), filename)


def event_hero_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path

    return get_random_upload_path(str(Path("uploads", "cycling_org", "event", "hero")), filename)


def event_attachment_file_path_func(instance, filename):
    from events.helpers import get_random_upload_path

    return get_random_upload_path(str(Path("uploads", "cycling_org", "event_attachment")), filename)


class Event(models.Model):
    """
    Name: This is the event name.
    blurb: This is a short un-formatted text about the event
    Description: This is long formatted
    Start_date: date and time.
    End_date: date and time.
    email: TODO: renamed to email
    country: defaults to usa.
    city: city, nearest of the event.
    state: state of the event.
    Website: Event website url.
    registration_website: URL where a user would register for the event.
    logo: Small image, logo for the event.
    # TODO: Move banner image out of json field to the hero field.
    hero: Large image, hero image for the event.
    Tags: List of event types
    more_data: Json data: Contains, TODO: move to panels json field.
    - panels: list of panels, like youtube or maps
    organization: the org that "owns" the event, used for sharing permissions.
    source: ? TODO: removed
    prefs: Json field
    - banner_image: The image to use as the banner TODO: use hero field
    - information_board_content: The content to show on the information board TODO: use Description field
    approved: BC admin must approve event for public viewing.
    """

    PUBLISH_TYPE_PUBLIC = "public"
    PUBLISH_TYPE_ORG_PUBLIC = "org_public"
    PUBLISH_TYPE_ORG_PRIVATE = "org_private"
    PUBLISH_TYPE_CHOICES = (
        (PUBLISH_TYPE_PUBLIC, "Public"),
        (PUBLISH_TYPE_ORG_PUBLIC, "Org Public"),
        (PUBLISH_TYPE_ORG_PRIVATE, "Org Private"),
    )
    name = models.CharField(max_length=200)
    blurb = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=300, null=True, blank=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    registration_website = models.URLField(max_length=500, null=True, blank=True)
    logo = models.ImageField(null=True, blank=True, upload_to=event_logo_file_path_func)
    hero = models.ImageField(null=True, blank=True, upload_to=event_hero_file_path_func)
    tags = ArrayField(
        models.CharField(max_length=100, blank=False, choices=event_types), size=50, null=True, blank=False
    )
    panels = models.JSONField(null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, related_name="events")
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    location_lat = models.FloatField(null=True, blank=True)
    location_lon = models.FloatField(null=True, blank=True)
    permit_no = models.CharField(max_length=25, blank=True)
    is_usac_permitted = models.BooleanField(default=False)
    featured_event = models.BooleanField(default=False)
    champion_event = models.BooleanField(default=False)
    approved = models.BooleanField(default=False, null=True)
    publish_type = models.CharField(max_length=32, choices=PUBLISH_TYPE_CHOICES)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class EventAttachment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="attachments", null=True, blank=False)
    file = models.FileField(upload_to=event_attachment_file_path_func)
    file_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.file_name

    def save(self, *args, **kwargs):
        self.file_name = self.file.name
        return super().save(*args, **kwargs)


class Race(models.Model):
    """
    name: this is the name of the race, Start Group, Field, etc.
    event: ForeignKey to event
    start_date: Start Day, optional
    start_time: Start Time, optional
    categories: List of categories, can be blank, or used to verify uploaded results if not blank.

    """

    name = models.CharField(max_length=256)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="races", null=True, blank=False)
    start_date = models.DateField(null=True, blank=False)
    start_time = models.TimeField(null=True, blank=True)
    categories = ArrayField(models.CharField(max_length=100, blank=False), size=50, null=True, blank=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = (("name", "event"),)

    def __str__(self):
        return f"{self.name}: {self.start_date}"

    @property
    def race_results(self):
        categories = set(self.raceresult_set.all().values_list("category", flat=True))
        for category in categories:
            yield category, self.raceresult_set.filter(category=category).order_by("place")


class RaceResult(models.Model):
    """
    rider: ForeignKey to member, create member is no match found.
        Try to match with usac_license, email, or name and date of birth
    name: Rider name, Combine first and last name on import if needed
    race: Another name would be race group or Start group.
    place: Finish place
    finish_status: OK, DNS (Did not start), DNF (Did not finish)
    category: the category the rider is competing in, might be different from Race.
    time: Elapsed time. optional treat as string
    gap: Gap to winner. optional treat as string
    bib_number: Bib number, optional
    usa_license: USAC license number, optional, used to match to member
    date_of_birth: Date of birth, optional, used to match to member
    club: Club name, optional, if we match to a user, we will fill this in from the user profile
    more_data: Extra columns uploaded with result, try to block PPI (email, phone, etc)
    create_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)"""

    FINISH_STATUS_OK = "ok"
    FINISH_STATUS_DNS = "dns"
    FINISH_STATUS_DNF = "dnf"
    FINISH_STATUS_CHOICES = (
        (FINISH_STATUS_OK, "OK"),
        (FINISH_STATUS_DNS, "DNS"),
        (FINISH_STATUS_DNF, "DNF"),
    )
    rider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="race_results")
    name = models.CharField(max_length=256, blank=False)
    race = models.ForeignKey(Race, on_delete=models.CASCADE, null=True, blank=False)
    place = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    finish_status = models.CharField(max_length=16, default=FINISH_STATUS_OK, choices=FINISH_STATUS_CHOICES)
    category = models.CharField(max_length=32, blank=False)
    time = models.CharField(max_length=32, blank=True)
    gap = models.CharField(max_length=32, blank=True)
    bib_number = models.CharField(max_length=32, blank=True)
    usac_license = models.CharField(max_length=32, blank=True)
    club = models.CharField(max_length=256, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    more_data = models.JSONField(
        null=True,
        blank=True,
    )
    create_datetime = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        unique_together = (("rider", "race"),)

    def __str__(self):
        return f"{self.place}--{self.name}--{self.rider}--{self.category}--Race: {self.race}"

    def save(self, *args, **kwargs):
        if not isinstance(self.place, int):
            self.place = None
            self.finish_status = self.place
        if not self.rider:
            self.rider = self.match_user(
                usac_license=self.usac_license,
                email=self.more_data.get("email", None),
                first_name=self.more_data.get("first_name", None),
                last_name=self.more_data.get("last_name", None),
                date_of_birth=self.date_of_birth,
            )
        return super().save(*args, **kwargs)

    @classmethod
    def match_user(cls, usac_license=None, email=None, first_name=None, last_name=None, date_of_birth=None):
        if usac_license:
            try:
                f = {"usac_license": usac_license, "usac_license_verified": True}
                return User.objects.get(**f)
            except User.DoesNotExist:
                pass
        if email:
            try:
                return User.objects.get(email=email)
            except User.DoesNotExist:
                pass
        if first_name and last_name and date_of_birth:
            try:
                return User.objects.get(first_name=first_name, last_name=last_name, date_of_birth=date_of_birth)
            except User.DoesNotExist:
                pass
        return None

    @property
    def points(self):
        try:
            return self.points_map[self.place - 1]
        except IndexError:
            pass
        except TypeError:
            pass

    @property
    def place_disp(self):
        if self.place:
            return self.place
        else:
            return self.finish_status

    # @property
    # def relative_place(self):
    #     """(Q(race=self.race) & Q(category=self.category) & Q(place__gte=self.place)"""
    #     try:
    #         if self.place:
    #             filter_dict = {"race": self.race, "category": self.category, "place__gte": self.place}
    #             return RaceResult.objects.filter(**filter_dict).count()
    #     except:
    #         return None

    # TODO: need to consolidate these club methods
    @property
    def usac_club(self):
        try:
            UsacDownload.objects.get(data__club__iexact=self.club)
            return True
        except UsacDownload.DoesNotExist:
            return False

    def usac_license_club(self):
        if self.usac_license:
            try:
                club = UsacDownload.objects.filter(license_number=self.usac_license)[0].data["club"]
                return club
            except Exception:
                logger.debug(f"Error getting club for {self.usac_license}")
                return None

    @property
    def bc_club(self):
        try:
            club = Organization.objects.get(name__iexact=self.club)
            return club
        except Organization.DoesNotExist:
            return None


def raceseries_logo_file_path_func(instance, filename):
    # Extract the file extension
    ext = filename.split(".")[-1]
    # Format the filename
    filename = f"{instance.id}_{filename}"
    return str(Path("uploads", "events", "event", "raceseries", "logo", f"{filename}.{ext}"))


class RaceSeries(models.Model):
    """
    name: Race Series name
    events = models.ManyToManyField(Event, related_name='race_series')
    races = models.ManyToManyField(Race, related_name='race_series')
    categories = ArrayField(
        models.CharField(max_length=100, blank=False),
        size=50,
        null=True,
        blank=False
    )
    points_map = models.JSONField(null=True, blank=True)
    ALGO = model_utils.Choices('Absolute', 'Relative') How points are calculated
    points_system = models.CharField(choices=ALGO, default=ALGO.Absolute, max_length=16, null=True, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='race_series')
    create_datetime = models.DateTimeField(auto_now_add=True)
    """

    POINTSYSTEM = [
        ("Absolute", "Absolute"),
        ("Relative", "Relative"),
    ]
    name = models.CharField(unique=True, max_length=256)
    events = models.ManyToManyField(Event, related_name="race_series")
    races = models.ManyToManyField(Race, related_name="race_series", blank=True)
    description = models.TextField(blank=True, default="")
    logo = models.ImageField(null=True, blank=True, upload_to=raceseries_logo_file_path_func)
    categories = ArrayField(models.CharField(max_length=100, blank=False), size=50, null=True, blank=False)
    points_map = models.JSONField(null=True, blank=True)  # this is a list, index position value = points
    point_system = models.CharField(choices=POINTSYSTEM, max_length=16, blank=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="race_series", null=True, blank=True
    )
    create_datetime = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    @property
    def all_results(self) -> list[RaceResult]:
        results = []
        for race in self.races.all():
            for result in race.raceresult_set.all():
                result.point_system = self.point_system
                result.points_map = self.points_map or list(reversed(range(1, 100)))
                results.append(result)
        return sorted(results, key=lambda x: x.name)

    @property
    def all_results_by_category(self) -> dict[str, list[RaceResult]]:
        all = self.all_results
        by_category = defaultdict(list)
        for result in all:
            # TODO: This is a bit of a hack until users are sign up
            if not result.club and result.usac_license:
                try:
                    # TODO: use the property for the result model.
                    result.club = (
                        UsacDownload.objects.order_by("create_datetime")
                        .filter(license_number=result.usac_license)[0]
                        .data["club"]
                    )
                except Exception as e:
                    logger.debug(f"Error getting club from UsacDownload {result.usac_license}: {e}")
                    pass

            by_category[result.category].append(result)
        return by_category

    @property
    def by_rider_points(self) -> dict:
        points = defaultdict(int)
        for _cat, result in self.all_results_by_category:
            points[result.rider] += result.points
        return points

    def by_license_points(self) -> dict:
        points = defaultdict(int)
        for result in self.all_results:
            try:
                int(result.license)
                points[result.license] += result.points
            except ValueError:
                pass
        return points

    @property
    def by_name_points(self) -> dict:
        all = self.all_results_by_category
        cat_results = {cat: {} for cat in all.keys()}
        for cat, results in self.all_results_by_category.items():
            for result in results:
                if result.name in cat_results[cat].keys():
                    if result.points:
                        cat_results[cat][result.name] += result.points
                else:
                    if result.points:
                        cat_results[cat][result.name] = result.points
        return cat_results
