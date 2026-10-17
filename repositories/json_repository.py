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


class DataBase(TypedDict):
    accounts : dict[str , bank_account.Bank_Account]
    categories : list[Category]
    transactions : list[Transaction]
    budgets : list[Budget]
    
    
class JSON_DataBase(TypedDict):
    accounts: dict[str, dict[str, str | int]]
    categories : list[dict[str,str]]
    transactions : list[dict[str,str]]
    budgets : list[dict[str,str]]
    
    
    


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



def save_db(data : DataBase) -> None:
    
    json_data : JSON_DataBase = {
        "accounts" : {},
        "categories" : [],
        "transactions" : [],
        "budgets" : []
    }
    
    with DB_PATH.open("r", encoding= "utf-8") as save_file:
        for account in data["accounts"]:
            name, bank_record = account.values()
            json_data["accounts"][name] = bank_record.get_keys()
        
            