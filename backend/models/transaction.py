from datetime import datetime


class Transaction:
    _id_counter = 0

    def __init__(self, user_id, stock, t_type, quantity, price):
        Transaction._id_counter += 1
        self._id = Transaction._id_counter
        self.user_id = user_id
        self.stock = stock
        self.type = t_type  # "BUY" or "SELL"
        self.quantity = quantity
        self.price = price
        self.date_time = datetime.now()
        self.total = quantity * price


    #Debugging and Clean message
    def __str__(self):
        return f"{self.type} {self.quantity} {self.stock.symbol} @ ${self.price:.2f}"

    def __repr__(self):
        return f"Transaction({self.type}, {self.stock.symbol}, {self.quantity}, {self.price})"