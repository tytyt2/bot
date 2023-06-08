import requests
import json


class ConvertionException(Exception):
    pass

class CConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозвожно перевести одинаковые валюты {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

        a = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote}{base}&key=26361c7ae9627554919bec896f67b31e')
        total_base = json.loads(a.content)['data'][f'{quote}{base}']
        count = float(total_base) * float(amount)
        return count