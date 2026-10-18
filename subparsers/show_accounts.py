from typing import Annotated

@add_subparser
def show_accounts(db : Database) -> None:
    
    for account_name in db["accounts"]:
        print(f"\n {account_name}: {type(db[account_name]["account"])} : {db[account_name]["account"].balance}")

        
    ...