from dataclasses import dataclass
from models.category import Category
from decimal import Decimal

@dataclass
class Budget:
    """Track a spending limit and current spend for a category."""

    category : Category
    limit_amount : Decimal
    spent_amount : Decimal
    
    
    def save_data(self) -> dict[str, object]:
        """Return the budget fields as JSON-compatible data."""
        return {
            "category" : self.category.save_data(),
            "limit_amount" : str(self.limit_amount),
            "spent_amount" : str(self.spent_amount),
        }

    def __str__(self) -> str:
        """Return a readable summary of the category budget."""
        return f"Category : {self.category}\nLimit: {self.limit_amount}\nSpent: {self.spent_amount}"