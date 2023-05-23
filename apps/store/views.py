# Create your views here.
import logging

import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from apps.store.models import Payment

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("EBC Store")


@csrf_exempt
def payment_webhook(request):
    """stripe trigger checkout.session.completed --add checkout_session:metadata.organization=orgapple"""

    # print("received webhook")
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        try:
            payment = {}
            data = event["data"]["object"]
            # print(json.dumps(data, indent=4, sort_keys=True))
            if data["metadata"].get("organization"):
                payment["organization"] = data["metadata"]["organization"]
            if data["metadata"].get("event"):
                payment["event"] = data["metadata"]["event"]
            payment["user"] = data["metadata"]["user"]
            payment["stripe_payment_id"] = data["payment_intent"]
            payment["stripe_customer_email"] = data["customer_details"]["email"]
            payment["amount"] = data["amount_total"]
            payment["payment_status"] = data["payment_status"]
            if data["metadata"].get("single_product"):
                payment["single_product"] = data["metadata"]["single_product"]
            Payment.objects.create(**payment)
        except Exception as e:
            logger.error(e)
            return HttpResponse(status=400)
    return HttpResponse(status=200)
