from backend.models.stock import Stock

class Transaction(Stock):

    def __init__(self, id, stock, types, price, date):
        super().__init__(id, )