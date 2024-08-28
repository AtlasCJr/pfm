from datetime import datetime

class Account:
    def __init__(self, username: str, 
                 password: str, security_question:int, 
                 security_answer:str, 
                 created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 updated_at: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                 balance:int = 0
                ) -> None:
        self.username = username
        self.password = password
        self.security_question = security_question
        self.security_answer = security_answer
        self.created_at = created_at
        self.updated_at = updated_at
        self.balance = balance

    def summary(self):
        print(f"{'Username':>15}: {self.username}")
        print(f"{'Password':>15}: {self.password}")
        print(f"{'Date Created':>15}: {self.created_at}")
        print(f"{'Date Updated':>15}: {self.updated_at}")
        print(f"{'Balance':>15}: {self.balance}")

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