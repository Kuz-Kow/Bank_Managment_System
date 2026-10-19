from models.account import Account


class Checking_Account(Account):
    
    def __init__(self, ID = None, balance = None):
        """Initialize a checking account with an optional ID and balance."""
        super().__init__(balance)
        if ID:
            self.account_id = ID
        else:
            self.account_id : str = "CAC" + f"{self._ID:3d}"
        self.commision = 0.02
        

    def withdraw(self, amount):
        """Withdraw an amount after applying the account commission."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Can't withdraw negative or zero amount!")
        return super().withdraw(round(amount * (1 + self.commision)))
    
    
    @classmethod
    def create_class_object(cls, **kwargs):
        """Create a checking account from serialized account fields."""
        return Checking_Account(**kwargs)

    def __str__(self):
        """Return a readable representation of the checking account."""
        return f"ID : {self.account_id}" +super().__str__() + f"commision: {self.commision}"