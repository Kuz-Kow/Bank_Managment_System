from models.account import Account



class Savings_Account(Account):
    
    def __init__(self):
        super().__init__()
        self.account_id : str = "SAC" + f"{self._ID:3d}"
        self.interest = 0.05
        
    def deposit(self, amount):
        return super().deposit(amount)
    
    def withdraw(self, amount):
        return super().withdraw((amount))
    
    def add_interest(self):
        self.balance += self.balance * self.interest