from __future__ import annotations

from typing import Never

class Money:
    
    _currencies : dict[str,int]= {
        "PLN" : 1,
        "USD" : 3.90,
        "EUR" : 4.3768,
        "UAH" : 0.087
    }
    
    
    def __init__(self, amount : int ,currency : str) -> None:
        """Create a non-negative monetary amount in a supported currency."""
        if amount < 0:
            raise ValueError("Amount cann't be negative")
        
        if currency not in self._currencies:
            raise ValueError("Not supported currencie")
        
        self._amount : int = amount
        self._currency : str = currency
        
        
    
    def convert(self, destin_currency) -> None:
        """Convert this amount to a supported destination currency."""
        if destin_currency not in self._currencies:
            raise ValueError("Not supported currencie")
        
        self.amount  = round(self.amount * self._currencies[destin_currency])
        self.currency = destin_currency
        
        
    @property
    def amount(self) -> int:
        """Return the amount in the smallest currency unit."""
        return self._amount
    
    @amount.setter
    def amount(self, value : int) -> None:
        """Set the amount, rejecting negative values."""
        if value < 0:
            raise ValueError("Amount cann't be negative")
        
        self._amount = value
        
        
    @amount.deleter
    def amount(self) -> Never:
        """Reject attempts to delete the amount."""
        raise ValueError("Cann't delete fields")
    
    
    @property
    def currency(self) -> str:
        """Return the currency code."""
        return self._currency
    
    
    @currency.setter
    def currency(self, curren : str) -> None:
        """Set the currency when it is supported."""
        if curren not in self._currencies:
            raise ValueError("Not supported currency")
            
    
    @amount.deleter
    def amount(self) -> Never:
        """Reject attempts to delete the amount."""
        raise ValueError("Cann't delete fields")
    
    
    def __str__(self) -> str:
        """Format the amount as a decimal value followed by its currency."""
        return f"{self.amount / 100:.2f}" + self.currency
        
    def __repr__(self):
        """Return a developer-oriented representation of this amount."""
        return type(self)+f"(amount = {self.amount}, currency = {self.currency})"
    
    def __eq__(self, value):
        """Compare this amount with another amount by converted value."""
        return (self.amount * self._currencies[self.currency]) == (value.amount * value._currencies[value.currency])
    
    def __lt__(self, other):
        """Compare monetary values, or compare against a raw amount."""
        if type(self) == type(other):
            return (self.amount * self._currencies[self.currency]) < (other.amount * other._currencies[other.currency])
        
        else:
            return self.amount < other
        
    def __add__(self, other: int | "Money") -> "Money":
        """Add an amount in this currency, converting another Money value if needed."""
        if isinstance(other, Money):
            other_in_pln = other.amount * self._currencies[other.currency]
            amount = round(other_in_pln / self._currencies[self.currency])
        elif isinstance(other, int):
            amount = other
        else:
            return NotImplemented

        return Money(amount=self.amount + amount, currency=self.currency)

    def __sub__(self, other: int | "Money") -> "Money":
        """Subtract an amount in this currency, converting another Money value if needed."""
        if isinstance(other, Money):
            other_in_pln = other.amount * self._currencies[other.currency]
            amount = round(other_in_pln / self._currencies[self.currency])
        elif isinstance(other, int):
            amount = other
        else:
            return NotImplemented

        return Money(amount=self.amount - amount, currency=self.currency)