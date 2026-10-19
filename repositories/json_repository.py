import json
import logging
from pathlib import Path
import tempfile
from typing import TypedDict
import re
from decimal import Decimal
from models.account import Account
from models.transaction import Transaction
from models.budget import Budget
from models.category import Category
from accounts import Bank_Account, Checking_Account, Savings_Account

DB_PATH = Path("db.json")
logger = logging.getLogger(__name__)

TAGS = {
        "ACC" : Bank_Account,
        "SAC" : Savings_Account,
        "CAC" : Checking_Account
}


class DataBase(TypedDict):
    accounts : dict[str, Account]
    categories : list[Category]
    transactions : list[Transaction]
    budgets : list[Budget]
    
    
class JSON_DataBase(TypedDict):
    accounts: dict[str, dict[str, object]]
    categories : list[dict[str, str]]
    transactions : list[dict[str, object]]
    budgets : list[dict[str, object]]
    
    
    


def load_db() -> DataBase:
    """Load the database from JSON, or return an empty database if none exists."""
    database : DataBase = {
                "accounts" : {},
                "categories" : [],
                "transactions" : [],
                "budgets" : []
            }
    
    if DB_PATH.is_file():
        with DB_PATH.open("r", encoding= "utf-8") as file:
            data : JSON_DataBase = json.load(file)
            

            for name, keys in data["accounts"].items():
                account_id = keys.get("ID")
                if not isinstance(account_id, str):
                    raise ValueError(f"Invalid account ID: {account_id}")
                match = re.match(r"^[A-Z]{3}", account_id)
                if match is None:
                    raise ValueError(f"Invalid account ID: {account_id}")
                prefix = match.group()
                if prefix not in TAGS:
                    raise ValueError(f"Unsupported account type prefix: {prefix}")
                database["accounts"][name] = TAGS[prefix].create_class_object(**keys)
                
            for categorie in data["categories"]:
                database["categories"].append(Category(**categorie))
                
                
            for budget in data["budgets"]:
                budget_data = dict(budget)
                category_data = budget_data.pop(
                    "category", budget_data.pop("categorie", None)
                )
                if isinstance(category_data, dict):
                    budget_data["category"] = Category(**category_data)
                budget_data["limit_amount"] = Decimal(
                    str(budget_data["limit_amount"])
                )
                budget_data["spent_amount"] = Decimal(
                    str(budget_data["spent_amount"])
                )
                database["budgets"].append(Budget(**budget_data))

            for transaction in data["transactions"]:
                transaction_data = dict(transaction)
                budget_category_name = transaction_data.pop("budget_category", None)
                category_data = transaction_data.pop(
                    "category", transaction_data.pop("categorie", None)
                )
                if isinstance(category_data, dict):
                    transaction_data["category"] = Category(**category_data)
                if budget_category_name is not None:
                    transaction_data["budget"] = _find_budget(
                        database["budgets"], str(budget_category_name)
                    )
                database["transactions"].append(Transaction(**transaction_data))
        logger.info(
            "Loaded database: %d accounts, %d categories, %d transactions, %d budgets",
            len(database["accounts"]),
            len(database["categories"]),
            len(database["transactions"]),
            len(database["budgets"]),
        )
    else:
        logger.info("Database file not found; starting with an empty database")

    return database


def _find_budget(budgets: list[Budget], category_name: str) -> Budget:
    """Return the sole budget for a category or raise when it is missing or ambiguous."""
    matches = [budget for budget in budgets if budget.category.name == category_name]
    if len(matches) != 1:
        raise ValueError(
            f"Expected exactly one budget for category '{category_name}', "
            f"found {len(matches)}"
        )
    return matches[0]



def save_db(data : DataBase) -> None:
    """Serialize the database contents to the configured JSON file."""
    
    json_data : JSON_DataBase = {
        "accounts" : {},
        "categories" : [],
        "transactions" : [],
        "budgets" : []
    }
    
    for name, account in data["accounts"].items():
        json_data["accounts"][name] = account.get_keys()

    for category in data["categories"]:
        json_data["categories"].append(category.save_data())

    for transaction in data["transactions"]:
        json_data["transactions"].append(transaction.save_data())

    for budget in data["budgets"]:
        json_data["budgets"].append(budget.save_data())

    serialized_data = json.dumps(json_data)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=DB_PATH.parent,
            prefix=f".{DB_PATH.name}.",
            suffix=".tmp",
            delete=False,
        ) as save_file:
            temporary_path = Path(save_file.name)
            save_file.write(serialized_data)
        temporary_path.replace(DB_PATH)
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
    logger.info(
        "Saved database: %d accounts, %d categories, %d transactions, %d budgets",
        len(data["accounts"]),
        len(data["categories"]),
        len(data["transactions"]),
        len(data["budgets"]),
    )