import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy
from stripe import ListObject

from config.helpers.Exception import exception

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def products() -> tuple[ListObject, list[str]]:
    products_list = stripe.Product.list(limit=100)
    errors = []
    for product in products_list:
        try:
            unit_amount_decimal = stripe.Price.retrieve(id=product["default_price"])["unit_amount_decimal"]
            unit_amount_decimal = float(unit_amount_decimal) / 100
        except ValueError:
            unit_amount_decimal = None
            # errors.append(f"ValueError: {product}")
        except stripe.error.InvalidRequestError:
            unit_amount_decimal = None
            # errors.append(f"stripe.error.InvalidRequestError: {product}")
        except stripe.error.APIConnectionError:
            unit_amount_decimal = None
            errors.append(f"stripe.error.APIConnectionError: {product}")
        # product["unit_amount_decimal"] = unit_amount_decimal
    return products_list, errors


def single_item_checkout(request, object) -> redirect:
    product = request.POST.get("single_product")
    metadata = {"single_product": "club_dues", "user": request.user.id}
    try:
        match product:
            case "club_dues":
                metadata["organization"] = object.id
                # the Club Dues product
                price_id = stripe.Product.retrieve("prod_NvhFVL6FC3AdKr")["default_price"]
                success_location = reverse_lazy("membership:organization_admin", kwargs={"pk": object.id})
                success_url = request.build_absolute_uri(location=success_location)
                cancel_location = reverse_lazy("membership:organization_admin", kwargs={"pk": object.id})
                cancel_url = request.build_absolute_uri(location=cancel_location)
            case "featured_event":
                metadata["event"] = object.id
                # price_id = stripe.Product.retrieve("prod_NvhFVL6FC3AdKr")["default_price"]
                # success_location = reverse_lazy("membership:organization_admin", kwargs={"pk": object.id})
                # success_url = request.build_absolute_uri(location=success_location)
                # cancel_location = reverse_lazy("membership:organization_admin", kwargs={"pk": object.id})
                # cancel_url = request.build_absolute_uri(location=cancel_location)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            customer_email=request.user.email,
            invoice_creation={"enabled": True},
            metadata=metadata,
            payment_intent_data={"metadata": metadata},
            phone_number_collection={"enabled": True},
            line_items=[
                {
                    # "name": f"Club Dues: {datetime.date.today().year}",
                    "price": price_id,
                    "quantity": 1,
                },
            ],
            mode="payment",
            success_url=success_url,
            cancel_url=cancel_url,
        )
    except Exception as e:
        exception(e)
    return checkout_session
