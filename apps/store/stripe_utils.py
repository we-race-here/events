import stripe
from django.shortcuts import redirect
from django.urls import reverse_lazy
from config.helpers.Exception import exception


def products() -> dict:
    products_list = stripe.Product.list(limit=100)
    for product in products_list:
        try:
            unit_amount_decimal = stripe.Price.retrieve(id=product["default_price"])["unit_amount_decimal"]
            unit_amount_decimal = float(unit_amount_decimal) / 100
        except ValueError:
            unit_amount_decimal = None
        product["unit_amount_decimal"] = unit_amount_decimal
    return products_list


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
