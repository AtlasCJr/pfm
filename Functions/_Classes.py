from uuid import uuid4 as randomID

class Account:
    def __init__(self, username: str, password: str, created_at: str, updated_at: str, balance, user_id: str = None) -> None:
        self.user_id = user_id if user_id is not None else str(randomID())
        self.username = username
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.balance = balance