from backend.models.user import User
from backend.models.portfolio import Portfolio
from backend.models.transaction import Transaction



class Account(User):

    def __init__(self, id, owner, balance):
        super().__init__(id, owner)
        self._balance = balance


