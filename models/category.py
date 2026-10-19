from dataclasses import dataclass

@dataclass
class Category:
    """Represent a named transaction or budget category."""

    name : str
    description : str
    
    
    def save_data(self) -> dict[str, str]:
        """Return the category fields as JSON-compatible data."""
        return {"name" : self.name, 
                "description" : self.description}

    def __str__(self):
        """Return the category name and description."""
        return f"Name : {self. name} \nDescription: {self.description}"