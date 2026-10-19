from models.account import Account


class Bank_Account(Account):

    def __init__(self, ID = None, balance = None):
        """Initialize a bank account with an optional ID and balance."""
        super().__init__(balance)
        if ID:
            self.account_id = ID
        else:
            self.account_id : str = "ACC" + f"{self._ID:3d}"
            

    
    @classmethod
    def create_class_object(cls, **kwargs):
        """Create a bank account from serialized account fields."""
        return Bank_Account(**kwargs)
    
    
    def __str__(self):
        """Return a readable representation of the bank account."""
        return f"ID : {self.account_id}" + super().__str__()