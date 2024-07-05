import requests
import json
from config import CRYPTOCOMPARE_API_URL

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        if base == quote:
            raise APIException("Невозможно перевести одинаковые валюты.")

        url = f'{CRYPTOCOMPARE_API_URL}?fsym={base.upper()}&tsyms={quote.upper()}'

        try:
            response = requests.get(url)
            data = json.loads(response.content)
        except Exception as e:
            raise APIException(f"Не удалось обработать запрос к API. Ошибка: {e}")

        if quote.upper() not in data:
            raise APIException(f"Валюта {quote} не найдена.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}.")

        return data[quote.upper()] * amount