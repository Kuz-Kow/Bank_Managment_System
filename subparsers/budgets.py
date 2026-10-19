from models.budget import Budget
from decimal import Decimal
from typing import Annotated
from repositories.json_repository import DataBase, save_db
from subparsers.parser import addparser


@addparser
def add_budget(db : DataBase, 
               category : Annotated[str, "Name of the category for the budget"],
               limit : Annotated[int, "Amount to spend on the category"]) -> None:
    """Create a budget for a category and persist the database."""
    categories = [item for item in db["categories"] if item.name == category]
    if len(categories) != 1:
        raise ValueError(
            f"Expected exactly one existing category named '{category}', "
            f"found {len(categories)}"
        )
    if any(budget.category.name == category for budget in db["budgets"]):
        raise ValueError(f"A budget already exists for category '{category}'")

    db["budgets"].append(
        Budget(
            category=categories[0],
            limit_amount=Decimal(limit),
            spent_amount=Decimal(0),
        )
    )
    save_db(db)
    
    
    
@addparser
def show_budgets(db : DataBase) -> None:
    """Print all budgets in the database."""
    for budget in db["budgets"]:
        print(budget)