from typing import Never

class Money:
    
    _currencies : dict[str,int]= {
        "PLN" : 1,
        "USD" : 3.90,
        "EUR" : 4.3768,
        "UAH" : 0.087
    }
    
    
    def __init__(self, amount : int ,currency : str) -> None:
        
        if amount < 0:
            raise ValueError("Amount cann't be negative")
        
        if currency not in self._currencies:
            raise ValueError("Not supported currencie")
        
        self._amount : int = amount
        self._currency : str = currency
        
        
    
    def convert(self, destin_currency) -> None:
        if destin_currency not in self._currencies:
            raise ValueError("Not supported currencie")
        
        self.amount  = round(self.amount * self._currencies[destin_currency])
        self.currency = destin_currency
        
        
    @property
    def amount(self) -> int:
        return self._amount
    
    @amount.setter
    def amount(self, value : int) -> None:
        if value < 0:
            raise ValueError("Amount cann't be negative")
        
        self._amount = value
        
        
    @amount.deleter
    def amount(self) -> Never:
        raise ValueError("Cann't delete fields")
    
    
    @property
    def currency(self) -> str:
        return self._currency
    
    
    @currency.setter
    def currency(self, curren : str) -> None:
        if curren not in self._currencies:
            raise ValueError("Not supported currency")
            
    
    @amount.deleter
    def amount(self) -> Never:
        raise ValueError("Cann't delete fields")
    
    
    def __str__(self) -> str:
            return f"{self.amount / 100:.2f}" + self.currency
        
    def __repr__(self):
        return type(self)+f"(amount = {self.amount}, currency = {self.currency})"
    
    def __eq__(self, value):
        return (self.amount * self._currencies[self.currency]) == (value.amount * value._currencies[value.currency])
    
    def __lt__(self, other):
        if type(self) == type(other):
            return (self.amount * self._currencies[self.currency]) < (other.amount * other._currencies[other.currency])
        
        else:
            return self.amount < other
        
    def __add__(self, other):
        
        amount = (self.amount * self._currencies[self.currency]) + (other.amount * other._currencies[other.currency])
        
        return Money(amount = amount, currency = "PLN")