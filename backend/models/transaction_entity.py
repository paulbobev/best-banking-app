from datetime import datetime
from enum import Enum

# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# Utilizing this transactiontype class makes it much simpler to label and extract
# str allows for string comparisons and enum keeps the values set
class TxnType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"

class Transaction:
    def __init__(self, txn_id: int, account_id: int, txn_type: TxnType, amount: Decimal, created_at: str):
        self.txn_id = txn_id
        self.account_id = account_id
        self.txn_type = txn_type
        self.amount = amount
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def get_dict(self) -> dict:
        return {"txn_id": self.txn_id, "account_id": self.account_id, "txn_type": self.txn_type.value, "amount": self.amount, "created_at": self.created_at}
