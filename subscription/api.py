import requests
import requests_cache

from currency_app.settings import EXCHANGE_URL, CURRENCIES
from subscription.exceptions import CurrencyException


requests_cache.install_cache('exchange_cache', backend='sqlite', expire_after=300)


def get_exchange(base_currency: str, exchange_date: str):
    base_currency = base_currency.upper()
    if base_currency not in CURRENCIES:
        raise CurrencyException

    if exchange_date is None:
        exchange_date = 'latest'

    url = f'{EXCHANGE_URL}/{exchange_date}?base={base_currency}'
    return requests.get(url).json()
