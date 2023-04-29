from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CharField, EmailField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from simple_history.models import HistoricalRecords

from events.users.managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for Events.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    SOCIAL_MEDIA_SCHEMA = {
        "zwift": {"type": "string", "required": False, "nullable": True, "meta": {"title": "Zwift"}},
        "zwiftpower": {"type": "string", "required": False, "nullable": True, "meta": {"title": "Zwift Power"}},
        "strava": {"type": "string", "required": False, "nullable": True, "meta": {"title": "Strava"}},
        "youtube": {"type": "string", "required": False, "nullable": True, "meta": {"title": "Youtube"}},
        "facebook": {"type": "string", "required": False, "nullable": True, "meta": {"title": "Facebook"}},
        "instagram": {"type": "string", "required": False, "nullable": True, "meta": {"title": "Instagram"}},
    }
    GENDER_MALE = "m"
    GENDER_FEMALE = "f"
    GENDER_OTHER = "o"
    GENDER_UNKNOWN = "u"
    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
        (GENDER_UNKNOWN, "Unknown"),
    )

    # First and last name do not cover name patterns around the globe
    # TODO: We need to use first and last name to match with USAC data.
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = EmailField(_("email address"), unique=True)
    username = None  # type: ignore
    usac_license = models.IntegerField(null=True, blank=True, unique=True)
    usac_license_verified = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=GENDER_UNKNOWN)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(blank=True, null=True)
    phone = PhoneNumberField(max_length=50, null=True, blank=True)
    phone_verified = models.BooleanField(default=None, null=True)
    address1 = models.CharField(max_length=256, blank=True, null=True)
    address2 = models.CharField(max_length=256, blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True)
    state = models.CharField(max_length=128, blank=True, null=True)
    zipcode = models.CharField(max_length=10, blank=True, null=True)
    weight = models.DecimalField(
        "Weight (kg)",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(10), MaxValueValidator(300)],
    )
    height = models.DecimalField(
        "Height (m)",
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
    )
    social_media = models.JSONField(null=True, blank=True)
    opt_in_email = models.BooleanField(default=False, null=True, blank=True)
    terms_of_service = models.BooleanField(default=False, null=True, blank=True)
    user_agreement_waiver = models.BooleanField(default=False, null=True, blank=True)
    # TODO: When user agrees to this, save HttpRequest.META to this field
    user_agreement_waiver_record = models.JSONField(null=True, blank=True)
    history = HistoricalRecords()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def age(self):
        if not self.birth_date:
            return
        return timezone.now().year - self.birth_date.year

    @property
    def full_name(self) -> str:
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
