from models.account import Account


class Bank_Account(Account):

    def __init__(self, ID = None, balance = None):
        super().__init__(balance)
        if ID:
            self.account_id = ID
        else:
            self.account_id : str = "ACC" + f"{self._ID:3d}"
            

    
    @classmethod
    def create_class_object(cls, **kwargs):
        return Bank_Account(**kwargs)
    
    
    def get_keys(self) -> dict[str, str | int]:
        return {"ID" : self.account_id, 
                "balance" : self.balance}
    