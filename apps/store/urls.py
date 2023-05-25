from django.urls import path

# now import the views.py file into this code
from . import views

urlpatterns = [
    path("", views.index),
    path("store/webhook/payments/", views.payment_webhook, name="payment_webhook"),
]
