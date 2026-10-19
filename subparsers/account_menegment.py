from typing import Annotated
from models.account import Account
from accounts.checking_account import Checking_Account
from accounts.bank_account import Bank_Account
from repositories.json_repository import save_db, DataBase
from accounts.savings_account import Savings_Account
from subparsers.parser import addparser


@addparser
def create_account(db : DataBase, name : Annotated[str, "Name of the account", []],
                  account_type : Annotated[str, "Type of the account", ["bank_account", "savings_account", "checking_account"]]):
    """Create the requested account type and persist the database."""
    
    match_account_type: dict[str, type[Account]] = {
        "bank_account" : Bank_Account,
        "savings_account" :  Savings_Account,
        "checking_account" : Checking_Account
    }

    if name in db["accounts"]:
        raise ValueError(f"Account with this name already exists: {name}")
            
    try:
        account_class = match_account_type[account_type]
    except KeyError as error:
        raise ValueError(f"Unsupported account type: {account_type}") from error

    db["accounts"][name] = account_class()
    save_db(db)
    
    
@addparser
def show_accounts(db : DataBase) -> None:
    """Print all named accounts in the database."""
    for name, account in db["accounts"].items():
        
        print(f"{name} : {account}")