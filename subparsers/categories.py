from models.category import Category
from typing import Annotated

@addsubparser
def create_category(db : Database, 
                    name : Annotated[str, "Name of the category", []], 
                    description : Annotated[str, "Description of the category", []]) -> None:
    
    db["categories"].append(Category(name = name,
                                     description= description))
    
    #save db
    
    
    

        