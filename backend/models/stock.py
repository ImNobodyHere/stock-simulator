class Stock:
    def __init__(self, symbol, name, current_price):
        self._symbol = symbol.upper()
        self._name = name
        self._current_price = current_price

    @property
    def symbol(self):
        return self._symbol

    @property
    def name(self):
        return self._name

    @property
    def current_price(self):
        return self._current_price

    @current_price.setter
    def current_price(self, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be non-negative")
        self._current_price = price


    #Debugging and Clean message
    def __str__(self):
        return f"{self._symbol}: ${self._current_price:.2f}"

    def __repr__(self):
        return f"Stock('{self._symbol}', '{self._name}', {self._current_price})"