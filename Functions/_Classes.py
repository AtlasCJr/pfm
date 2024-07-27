from uuid import uuid4 as randomID

class Account:
    def __init__(self, username, password, created_at, updated_at, balance) -> None:
        self.username = username
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.balance = balance
        self.user_id = str(randomID())