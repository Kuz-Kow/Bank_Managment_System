from models.transaction import Transaction
from utils.money import Money 


class Account:

    _ID : int = 0
    
    def __init__(self, balance : dict[str, int | str]):
        self._ID +=1
        
        if balance:
            self.__balance : float = Money(balance["amount"], balance["currency"])
        else:
            self.__balance : float = Money(0, "PLN")
            
        
    @property    
    def balance(self):
        return {"amount" : self.__balance.amount, 
                "currency" : self.__balance.currency}
    
    @balance.setter
    def balance(self, amount):
        raise ValueError("Can't change balance directli")
        
    
    @balance.deleter
    def balance(self, amount):
        raise ValueError("Can't delete balance field")
    
    def deposit(self, amount : int):
        if not amount > 0:
            raise ValueError("Can't deposit negative amount or zero!")
        
        self.__balance += amount 
        
    
    def withdraw(self, amount : int):
        if not amount > 0:
            raise ValueError("Can't withdraw negative or zero amount!")
        
        if amount > self.__balance:
            raise ValueError("Not enough money on the account")
        
        
        self.__balance -= amount
        

        
        
    