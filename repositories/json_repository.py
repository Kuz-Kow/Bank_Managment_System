import json
from pathlib import Path
from typing import TypedDict
import re
from models.transaction import Transaction
from models.budget import Budget
from models.category import Category
from accounts import Bank_Account, Checking_Account, Savings_Account

DB_PATH = Path("db.json")

TAGS = {
        "ACC" : Bank_Account,
        "SAC" : Savings_Account,
        "CAC" : Checking_Account
}


class DataBase(TypedDict):
    accounts : dict[str , Bank_Account]
    categories : list[Category]
    transactions : list[Transaction]
    budgets : list[Budget]
    
    
class JSON_DataBase(TypedDict):
    accounts: dict[str, dict[str, str | int]]
    categories : list[dict[str,str]]
    transactions : list[dict[str,str]]
    budgets : list[str]
    
    
    


def load_db() -> DataBase:
    
    database : DataBase = {
                "accounts" : {},
                "categories" : [],
                "transactions" : [],
                "budgets" : []
            }
    
    if DB_PATH.is_file():
        with DB_PATH.open("r", encoding= "utf-8") as file:
            data : JSON_DataBase = json.load(file)
            

            for account in data["accounts"].items():
                name, keys = account.values()
                prefix = re.match(r"^[A-Z]{3}", keys["ID"]).group()
                database["accounts"][name] = TAGS[prefix].create_class_object(**keys)
                
            for categorie in data["categories"]:
                database["categories"].append(Category(**categorie))
                
                
            for transaction in data["transactions"]:
                transaction[categorie] = Category(**transaction.pop("categorie"))
                database["transactions"].append(Transaction(**transaction))
                
            
            for budget in data["budgets"]: 
                budget["categorie"] = Category(**budget.pop("categorie"))
                database["budgets"].append(Budget(**budget))
                
            
        

        
    return database



def save_db(data : DataBase) -> None:
    
    
    json_data : JSON_DataBase = {
        "accounts" : {},
        "categories" : [],
        "transactions" : [],
        "budgets" : []
    }
    
    with DB_PATH.open("w", encoding= "utf-8") as save_file:
        for account in data["accounts"]:
            name, bank_record = account.values()
            json_data["accounts"][name] = bank_record.get_keys()
        
            
        for categorie in data["categories"]:
            json_data["categories"].append(categorie.save_data())
            
        for transaction in data["transactions"]:
            json_data["transactions"].append(transaction.save_data())
            
            
        for budget in data["budgets"]:
            json_data["budgets"].append(budget.save_data())
            
        json.dump(json_data, save_file)