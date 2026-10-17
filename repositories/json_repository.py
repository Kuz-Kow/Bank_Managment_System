import json
from pathlib import Path
from typing import TypedDict
from models.transaction import Transaction
from models.budget import Budget
from models.category import Category
from accounts import bank_account, checking_account, savings_account
import re


DB_PATH = Path("db.json")

TAGS = {
        "ACC" : bank_account.Bank_Account,
        "SAC" : savings_account.Savings_Account,
        "CAC" : checking_account.Checking_Account
}


class Database(TypedDict):
    accounts : dict[str , bank_account.Bank_Account]
    categories : list[Category]
    transactions : list[Transaction]
    budgets : list[Budget]
    


def load_db(path : Path) -> Database:
    
    database : Database = {
                "accounts" : {},
                "categories" : [],
                "transactions" : [],
                "budgets" : []
            }
    
    if DB_PATH.is_file():
        with DB_PATH.open("r", encoding= "utf-8") as file:
            data = json.load(file)
            

            for account in data["accounts"]:
                name, keys = account.values()
                prefix = re.match(r"^[A-Z]{3}", keys["ID"]).group()
                database["accounts"][name] = TAGS[prefix].create_class_object(**keys)
                
            for categorie in data["categories"]:
                database["categories"].append(Category(categorie.values[0], categorie.values[1]))
                
                
            for transaction in data["transactions"]:
                database["transactions"].append(Transaction(**transaction))
                
            
            for budget in data["budgets"]: 
                database["budgets"].append(Budget(**budget))
                
            
        

        
    return database