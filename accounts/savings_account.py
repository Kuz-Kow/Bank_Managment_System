from models.account import Account



class Savings_Account(Account):
    
    def __init__(self, ID = None, balance = None):
        super().__init__(balance)
        if ID:
            self.account_id = ID
        else:
            self.account_id : str = "SAC" + f"{self._ID:3d}"
            
        self.interest = 0.05

    
    def add_interest(self):
        self.balance += self.balance * self.interest
        
        
    @classmethod
    def create_class_object(cls, **kwargs):
        return Savings_Account(**kwargs)