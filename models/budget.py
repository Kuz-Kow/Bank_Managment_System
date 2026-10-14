from dataclasses import dataclass
from models.category import Category
from decimal import Decimal

@dataclass
class Budget:
    category : Category
    limit_amount : Decimal
    spent_amount : Decimal
    period : str