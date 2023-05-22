import stripe


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
