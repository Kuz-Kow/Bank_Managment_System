from typing import Annotated
from sys import exit
from models.account import Account
from accounts.checking_account import Checking_Account
from accounts.bank_account import Bank_Account
from accounts.savings_account import Savings_Account

@add_subparser
def create_account(db : Database, name : Annotated[str, "Name of the account", []],
                  account_type : Annotated[str, "Type of the account", ["bank_account", "savings_account", "checking_account"]]):
    
    
    match_account_type : dict[str, Account] = {
        "bank_account" : Bank_Account,
        "savings_account" :  Savings_Account,
        "checking_account" : Checking_Account
    }

    
    if db["accounts"][name]:
            exit("Account with this name is alredy exists")
            
            
    db["accounts"][name] = match_account_type[account_type]()
    
    ...