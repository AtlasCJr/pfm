class Account:
    def __init__(self, username: str, password: str, created_at: str, updated_at: str, balance) -> None:
        self.username = username
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at
        self.balance = balance

    def summary(self):
        print(f"""
            {'Username':>20}: {self.username}
            {'Password':>20}: {self.password}
            {'Date Created':>20}: {self.created_at}
            {'Date Updated':>20}: {self.updated_at}
            {'Balance':>20}: {self.balance}
        """)

typeMapping = {
    0: "Foods & Drinks",
    1: "Transportation",
    2: "Entertainment", 
    3: "Healthcare",
    4: "Asurance",
    5: "Luxury",
    10: "Fixed Income",
    11: "Passive Income",
    12: "Invest Income",
    13: "Other Income"
}