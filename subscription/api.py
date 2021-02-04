import requests
from currency_app.settings import EXCHANGE_URL, BASE_CURRENCY, CURRENCIES
from subscription.exceptions import CurrencyException


def get_exchange(base_currency: str):
    base_currency = base_currency.upper()
    if base_currency not in CURRENCIES:
        raise CurrencyException

    url = f'{EXCHANGE_URL}/latest?base={base_currency}'
    return requests.get(url).json()
