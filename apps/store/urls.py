from django.urls import path

# now import the views.py file into this code
from . import views
from .views import StripeAccounting

app_name = "store"
urlpatterns = [
    path("", views.index),
    path("store/webhook/payments/", views.payment_webhook, name="payment_webhook"),
    path("store/stripe_accounting/", StripeAccounting.as_view(), name="stripe_accounting"),
]
