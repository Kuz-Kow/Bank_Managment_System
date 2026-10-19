from typing import Protocol

class Money_Account(Protocol):
    
    """Describe an account that supports deposits and withdrawals."""

    def withdraw(self, amount) -> None:
        """Withdraw an amount from the account."""
        ...
    
    def deposit(self, amount) -> None:
        """Deposit an amount into the account."""
        ...