from models.account import Account



class Savings_Account(Account):
    
    def __init__(self, ID = None, balance = None):
        """Initialize a savings account with an optional ID and balance."""
        super().__init__(balance)
        if ID:
            self.account_id = ID
        else:
            self.account_id : str = "SAC" + f"{self._ID:3d}"
            
        self.interest = 0.05

    
    def add_interest(self):
        """Add the account's configured interest to its balance."""
        self.balance += self.balance * self.interest
        
        
    @classmethod
    def create_class_object(cls, **kwargs):
        """Create a savings account from serialized account fields."""
        return Savings_Account(**kwargs)

    def __str__(self):
        """Return a readable representation of the savings account."""
        return f"ID : {self.account_id}" + super().__str__() + f"interest: {self.interest}"