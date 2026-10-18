from dataclasses import dataclass
from models.category import Category

@dataclass
class Transaction:
    sender : str
    reciever : str
    amount : int
    details : str
    transaction_time : str
    category : Category
    
    
    def save_data(self) -> dict[str, str]:
        return {"sender" : self.sender,
                "reciever" : self.reciever,
                "amount" : self.amount,
                "details" : self.details,
                "transaction_time" : self.transaction_time,
                "category" : self.category.save_data()}