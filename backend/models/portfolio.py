from datetime import datetime
from backend.models.account import Account
from backend.models.stock import Stock
from backend.models.transaction import Transaction


class Portfolio(Account):
    _id_counter = 0
    def __init__(self, id, owner, name):
        Portfolio._id_counter += 1
        super().__init__(id, owner, 10000)
        self.__created_at =  datetime.now()


    def buy_stock(self, stock: Stock, quantity: float):
        pass

    def sell_stock(self, stock: Stock, quantity: float):
        pass

    def get_holdings(self):
        pass

    def get_total_values(self):
        pass