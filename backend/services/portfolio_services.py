from backend.models.user import User
from backend.models.stock import Stock
from backend.models.transaction import Transaction
from backend.models.position import Position
from backend.exceptions import InsufficientBalanceError, InsufficientSharesError
from functools import reduce
from itertools import islice


class PortfolioService:
    def __init__(self):
        self.users = {}
        self.stocks = {}
        self.transactions = []
        self.positions = {}

    # User management
    def create_user(self, username, email, password, balance=10000):
        user = User(username, email, password, balance)
        self.users[user.id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    # Stock management
    def add_stock(self, symbol, name, price):
        stock = Stock(symbol, name, price)
        self.stocks[symbol.upper()] = stock
        return stock

    def get_stock(self, symbol):
        return self.stocks.get(symbol.upper())

    def get_user_transactions(self, user_id):
        for transaction in self.transactions:
            if transaction.user_id == user_id:
                yield transaction

    def get_recent_transactions(self, user_id, limit=5):
        trans_gen = self.get_user_transactions(user_id)
        return list(islice(trans_gen, limit))

    # Buy stock
    def buy_stock(self, user_id, symbol, quantity):
        user = self.get_user(user_id)
        stock = self.get_stock(symbol)

        if not stock:
            raise ValueError(f"Stock {symbol} not found")

        total_cost = quantity * stock.current_price

        # Use custom exception
        if user.balance < total_cost:
            raise InsufficientBalanceError(f"Need ${total_cost:.2f}, have ${user.balance:.2f}")

        # Deduct balance
        user.deduct_balance(total_cost)

        # Create transaction
        transaction = Transaction(user_id, stock, "BUY", quantity, stock.current_price)
        self.transactions.append(transaction)

        # Update position
        if user_id not in self.positions:
            self.positions[user_id] = {}

        if symbol in self.positions[user_id]:
            self.positions[user_id][symbol].add_shares(quantity, stock.current_price)
        else:
            self.positions[user_id][symbol] = Position(user_id, stock, quantity, stock.current_price)

        return transaction

    # Sell stock
    def sell_stock(self, user_id, symbol, quantity):
        user = self.get_user(user_id)
        stock = self.get_stock(symbol)

        if user_id not in self.positions or symbol not in self.positions[user_id]:
            raise InsufficientSharesError(f"You don't own {symbol}")

        position = self.positions[user_id][symbol]

        if position.quantity < quantity:
            raise InsufficientSharesError(f"You only have {position.quantity} shares")

        # Calculate revenue
        total_revenue = quantity * stock.current_price

        # Add balance
        user.add_balance(total_revenue)

        # Create transaction
        transaction = Transaction(user_id, stock, "SELL", quantity, stock.current_price)
        self.transactions.append(transaction)

        # Update position
        position.remove_shares(quantity)
        if position.quantity == 0:
            del self.positions[user_id][symbol]

        return transaction

    def get_portfolio(self, user_id):
        return self.positions.get(user_id, {})

    def get_portfolio_value(self, user_id):
        positions = self.get_portfolio(user_id).values()
        values = map(lambda p: p.get_current_value(), positions)
        return reduce(lambda acc, val: acc + val, values, 0)

    def get_profitable_positions(self, user_id):
        positions = self.get_portfolio(user_id).values()
        return list(filter(lambda p: p.get_profit_loss() > 0, positions))

    def calculate_total_profit_loss(self, user_id):
        positions = self.get_portfolio(user_id).values()
        return reduce(lambda acc, p: acc + p.get_profit_loss(), positions, 0)