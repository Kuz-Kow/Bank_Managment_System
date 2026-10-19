from models.transaction import Transaction
from utils.money import Money 


class Account:

    _ID : int = 0
    account_id: str
    
    def __init__(self, balance: dict[str, int | str] | None = None):
        """Initialize an account from serialized balance data, if provided."""
        self._ID +=1
        
        if balance:
            self.__balance: Money = Money(balance["amount"], balance["currency"])
        else:
            self.__balance: Money = Money(0, "PLN")
            
        
    @property    
    def balance(self) -> dict[str, int | str]:
        """Return the balance as an amount and currency mapping."""
        return {"amount" : self.__balance.amount, 
                "currency" : self.__balance.currency}
    
    @balance.setter
    def balance(self, amount):
        """Reject direct assignment to the account balance."""
        raise ValueError("Can't change balance directli")
        
    
    @balance.deleter
    def balance(self, amount):
        """Reject attempts to delete the account balance."""
        raise ValueError("Can't delete balance field")
    
    def deposit(self, amount : int):
        """Deposit a positive amount into the account."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Can't deposit negative amount or zero!")
        
        self.__balance = self.__balance + amount
        
    
    def withdraw(self, amount : int):
        """Withdraw a positive amount if the account has sufficient funds."""
        if not isinstance(amount, int) or amount <= 0:
            raise ValueError("Can't withdraw negative or zero amount!")
        
        if amount > self.__balance.amount:
            raise ValueError("Not enough money on the account")
        
        
        self.__balance = self.__balance - amount

    def get_keys(self) -> dict[str, object]:
        """Return the account fields used for JSON serialization."""
        return {"ID": self.account_id, "balance": self.balance}

    def __str__(self) -> str:
        """Return a readable representation of the account and its balance."""
        return f"{type(self)} : {self.balance}"
    