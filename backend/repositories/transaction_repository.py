# repositories/transaction_repository.py
from datetime import datetime
from decimal import Decimal
from bson.decimal128 import Decimal128
from db import accounts_collection as accounts_col, transactions_collection as txns_col, get_next_id
from models.transaction_entity import Transaction


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _to_txn(doc) -> Transaction:
    return Transaction(
        doc["txn_id"],
        doc["account_id"],
        doc["txn_type"],
        doc["amount"].to_decimal(),
        doc.get("created_at"),
    )


class TransactionRepository:

    def deposit(self, account_id: int, amount: Decimal) -> int:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        acct = accounts_col.find_one({"_id": account_id}, {"balance": 1})
        if acct is None:
            raise ValueError(f"Account {account_id} not found")
        new_balance = acct["balance"].to_decimal() + amount
        accounts_col.update_one(
            {"_id": account_id},
            {"$set": {"balance": Decimal128(str(new_balance))}},
        )
        txn_id = get_next_id("transactions")
        txns_col.insert_one({
            "_id": txn_id, "txn_id": txn_id, "account_id": account_id,
            "txn_type": "DEPOSIT", "amount": Decimal128(str(amount)),
            "created_at": _now(),
        })
        return txn_id

    def withdraw(self, account_id: int, amount: Decimal) -> int:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        acct = accounts_col.find_one({"_id": account_id}, {"balance": 1})
        if acct is None:
            raise ValueError(f"Account {account_id} not found")
        balance = acct["balance"].to_decimal()
        if balance < amount:
            raise ValueError("Insufficient funds")
        accounts_col.update_one(
            {"_id": account_id},
            {"$set": {"balance": Decimal128(str(balance - amount))}},
        )
        txn_id = get_next_id("transactions")
        txns_col.insert_one({
            "_id": txn_id, "txn_id": txn_id, "account_id": account_id,
            "txn_type": "WITHDRAW", "amount": Decimal128(str(amount)),
            "created_at": _now(),
        })
        return txn_id

    def find_by_id(self, txn_id: int) -> Transaction | None:
        doc = txns_col.find_one({"_id": txn_id})
        return _to_txn(doc) if doc else None

    def find_by_account(self, account_id: int) -> list[Transaction]:
        return [_to_txn(d) for d in
                txns_col.find({"account_id": account_id}).sort("_id", -1)]