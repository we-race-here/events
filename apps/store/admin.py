from django.contrib import admin

from apps.store import models


# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "event", "amount", "payment_status", "single_product", "create_datetime")
    list_filter = ("single_product",)
    search_fields = ("user__first_name", "user__last_name", "organization__name", "event__name", "stripe_payment_id")


# Register your models here.
admin.site.register(models.Payment, PaymentAdmin)
