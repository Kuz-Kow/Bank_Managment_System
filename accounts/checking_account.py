from models.account import Account


class Checking_Account(Account):
    
    def __init__(self, ID = None, balance = None):
        super().__init__(balance)
        if ID:
            self.account_id = ID
        else:
            self.account_id : str = "CAC" + f"{self._ID:3d}"
        self.commision = 0.02
        

    def withdraw(self, amount):
        return super().withdraw((amount + amount * self.commision))
    
    
    @classmethod
    def create_class_object(cls, **kwargs):
        return Checking_Account(**kwargs)