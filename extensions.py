import requests
import json


class APIExtension(Exception):
    def __init__(self, text):
        self.txt = text


class CryptoComp:
    @staticmethod
    def get_prices(base, quote, amount):
        crypto_data = requests.get(
            "https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}".format(base,quote)).json()['RAW']
        crypto_data = json.dumps(crypto_data)
        load_data = json.loads(crypto_data)
        price = load_data[base][quote]["PRICE"] * amount
        return round(price)


if __name__ == "__main__":
    a = CryptoComp()
    print(a.get_prices('EUR', 'RUB', 100))