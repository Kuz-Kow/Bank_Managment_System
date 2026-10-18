from dataclasses import dataclass

@dataclass
class Category:
    name : str
    description : str
    
    
    def save_data(self) -> dict[str, str]:
        return {"name" : self.name, 
                "description" : self.description}