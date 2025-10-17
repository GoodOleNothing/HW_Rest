import requests
from django.conf import settings


HEADERS = {
    "Authorization": f"Bearer {settings.STRIPE_API_KEY}"
}


def create_stripe_product(name: str):
    """Создание продукта в Stripe"""
    url = f"{settings.STRIPE_BASE_URL}/products"
    data = {"name": name}
    response = requests.post(url, headers=HEADERS, data=data)
    response.raise_for_status()
    return response.json()


def create_stripe_price(product_id: str, amount: float):
    """Создание цены в Stripe (в копейках)"""
    url = f"{settings.STRIPE_BASE_URL}/prices"
    data = {
        "unit_amount": int(amount * 100),  # копейки
        "currency": "rub",
        "product": product_id,
    }
    response = requests.post(url, headers=HEADERS, data=data)
    response.raise_for_status()
    return response.json()


def create_stripe_session(price_id: str, success_url: str, cancel_url: str):
    """Создание checkout-сессии"""
    url = f"{settings.STRIPE_BASE_URL}/checkout/sessions"
    data = {
        "payment_method_types[]": "card",
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1,
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url,
    }
    response = requests.post(url, headers=HEADERS, data=data)
    response.raise_for_status()
    return response.json()