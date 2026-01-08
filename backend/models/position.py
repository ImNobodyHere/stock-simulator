class Position:
    def __init__(self, user_id, stock, quantity, average_price):
        self.user_id = user_id
        self.stock = stock
        self.quantity = quantity
        self.average_price = average_price

    def get_current_value(self):
        return self.quantity * self.stock.current_price

    def get_cost_basis(self):
        return self.quantity * self.average_price

    def get_profit_loss(self):
        return self.get_current_value() - self.get_cost_basis()

    def add_shares(self, quantity, price):
        total_cost = self.get_cost_basis() + (quantity * price)
        self.quantity += quantity
        self.average_price = total_cost / self.quantity

    def remove_shares(self, quantity):
        if quantity > self.quantity:
            raise ValueError("Cannot sell more than owned")
        self.quantity -= quantity


    #Debugging and Clean message
    def __str__(self):
        return f"{self.stock.symbol}: {self.quantity} shares @ ${self.average_price:.2f}"

    def __repr__(self):
        return f"Position({self.stock.symbol}, {self.quantity}, {self.average_price})"