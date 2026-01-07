from datetime import datetime

class Stock:

    def __init__(self, symbol, price, currency):
        self._symbol = symbol
        self._price = price
        self._currency = currency
        self._created_at = datetime.now()
        self._updated_at = datetime.now()


    def update_price(self, new_price: float):
        if new_price < 0:
            raise ValueError("Error: price of stock cannot be negative")

        self._price = new_price
