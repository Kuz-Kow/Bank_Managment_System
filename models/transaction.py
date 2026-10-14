from dataclasses import dataclass

@dataclass
class Transaction:
    sender : str
    reciever : str
    amount : int
    details : str
    transaction_time : str