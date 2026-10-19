from dataclasses import dataclass
from models.budget import Budget
from models.category import Category

@dataclass
class Transaction:
    """Represent a payment and, for new payments, its associated budget."""

    sender : str
    reciever : str
    amount : int
    details : str
    transaction_time : str
    category : Category
    budget : Budget | None = None
    
    
    def save_data(self) -> dict[str, object]:
        """Return the transaction as JSON-compatible data."""
        data: dict[str, object] = {
            "sender": self.sender,
            "reciever": self.reciever,
            "amount": self.amount,
            "details": self.details,
            "transaction_time": self.transaction_time,
            "category": self.category.save_data(),
        }
        if self.budget is not None:
            data["budget_category"] = self.budget.category.name
        return data