from datetime import datetime
import re

class User:
    _id_counter = 0
    def __init__(self, username, email, password):
        User._id_counter += 1
        self._username = username
        self._email = email
        self._password = password
        self._created_at = datetime.now()

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def password(self):
        return self._password

    @property
    def get_date(self):
        return self._created_at

    @username.setter
    def username(self, name: str):
        if name.isdigit() or len(name) < 4:
            raise NameError("Error: Name is invalid.")
        else:
            self._username = name

    @email.setter
    def email(self, e: str):
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if re.match(pattern, e) is None:
            raise ValueError("Error: incorrect email.")
        else:
            self._email = e

    @password.setter
    def password(self, pw: str):
        if len(pw) < 8:
            raise ValueError("Error: The password is too short.")
        else:
            self._password = pw

