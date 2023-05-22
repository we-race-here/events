from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint

from apps.event.models import Event
from apps.membership.models import Organization

User = get_user_model()


# Create your models here.
class Payment(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_payment_id = models.CharField(max_length=255, blank=False, null=False)
    stripe_customer_email = models.EmailField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    single_product = models.CharField(max_length=255)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-create_datetime"]
        constraints = [
            UniqueConstraint(fields=["stripe_payment_id", "payment_status"], name="unique payment"),
        ]

    def __str__(self):
        return self.stripe_payment_id

    @property
    def stripe_link(self):
        return f"https://dashboard.stripe.com/payments/{self.stripe_payment_id}"
