from models.category import Category
from typing import Annotated
from repositories.json_repository import save_db, DataBase
from subparsers.parser import addparser


@addparser
def create_category(db : DataBase,
                    name : Annotated[str, "Name of the category"],
                    description : Annotated[str, "Description of the category"]) -> None:
    """Create a category, add it to the database, and save the database."""
    db["categories"].append(Category(name = name,
                                     description= description))
    
    save_db(db)
    
@addparser
def show_categories(db : DataBase) -> None:
    """Print all categories in the database."""
    for categorie in db["categories"]:
        print(categorie)