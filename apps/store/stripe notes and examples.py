checkout_session = stripe.checkout.Session.create(
    payment_method_types=["card"],
    customer_email="v@vdavis.net",
    invoice_creation={"enabled": True},
    metadata={"club_dues": "2023_test"},
    payment_intent_data={"metadata": {"club_dues": "2023_test"}},
    line_items=[
        {
            "price_data": {
                "currency": "usd",
                "unit_amount": 123,
                "product_data": {
                    "name": "2023 Club Dues",
                    "description": "You club dues for 2023",
                    # "images": ["https://example.com/t-shirt.png"],
                },
            },
            "quantity": 1,
        }
    ],
    mode="payment",
    success_url="http://localhost:8000/org/10/",
    cancel_url="http://localhost:8000/org/10/",
)
