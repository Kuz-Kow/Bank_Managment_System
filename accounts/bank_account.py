from models.account import Account


class Bank_Account(Account):

    def __init__(self):
        super().__init__()
        self.account_id : str = "ACC" + f"{self._ID:3d}"
    
    def deposit(self, amount):
        return super().deposit(amount)
        
    
    def withdraw(self, amount : int):
        return super().withdraw(amount)
        
    