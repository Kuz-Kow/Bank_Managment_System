from models.account import Account


class Checking_Account(Account):
    
    def __init__(self):
        super().__init__()
        self.account_id : str = "SAC" + f"{self._ID:3d}"
        self.commision = 0.02
        
    def deposit(self, amount):
        return super().deposit(amount)
    
    def withdraw(self, amount):
        return super().withdraw((amount + amount * self.commision))