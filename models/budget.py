from dataclasses import dataclass
from models.category import Category
from decimal import Decimal

@dataclass
class Budget:
    category : Category
    limit_amount : Decimal
    spent_amount : Decimal
    period : str
    
    
    def save_data(self) -> dict:
        return {
            "category" : self.category.save_data(),
            "limit_amount" : self.limit_amount,
            "spent_amount" : self.spent_amount,
            "period" : self.period
        }