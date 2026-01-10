from datetime import datetime

class User:
    _id_counter = 0

    def __init__(self, username, password, balance=10000.0):
        User._id_counter += 1
        self._id = User._id_counter
        self._username = username
        self._password = password
        self._balance = balance
        self._created_at = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Balance must be non-negative")
        self._balance = amount

    def deduct_balance(self, amount):
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount

    def add_balance(self, amount):
        self._balance += amount



    #Debugging and Clean message
    def __str__(self):
        return f"User({self._username}, balance=${self._balance:.2f})"

    def __repr__(self):
        return f"User(id={self._id}, username='{self._username}', balance={self._balance})"