from models.transaction import Transaction
from utils.money import Money 
    

class Account:

    _ID : int = 0
    
    def __init__(self):
        self._ID +=1
        self.__balance : float = Money(0, "PLN")
        self._transactions : list[Transaction] = []
        
    @property    
    def balance(self):
        return self.__balance
    
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
        
    