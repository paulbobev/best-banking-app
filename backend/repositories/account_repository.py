# repositories/account_repository.py
from decimal import Decimal
from db import get_cursor
from models.account_entity import Account


class AccountRepository:

    def create(self, user_id: int, account_type: str, initial_balance: Decimal = Decimal("0.00")) -> int:
        with get_cursor(commit=True) as cur:
            cur.execute(
                "INSERT INTO accounts (user_id, account_type, balance) VALUES (?, ?, ?)",
                (user_id, account_type, initial_balance),
            )

            account_id = cur.lastrowid
            if account_id is None:
                raise RuntimeError("Account insert did not return an ID")

            return int(account_id)

    def find_by_id(self, account_id: int) -> Account | None:
        with get_cursor() as cur:
            cur.execute(
                "SELECT account_id, user_id, account_type, balance, created_at "
                "FROM accounts WHERE account_id = ?",
                (account_id,),
            )
            row = cur.fetchone()
            if row is None:
                return None
            return Account(
                row["account_id"],
                row["user_id"],
                row["account_type"],
                row["balance"],
                row["created_at"],
            )

    def find_by_user(self, user_id: int) -> list[Account]:
        with get_cursor() as cur:
            cur.execute(
                "SELECT account_id, user_id, account_type, balance, created_at "
                "FROM accounts WHERE user_id = ? ORDER BY account_id",
                (user_id,),
            )
            return [
                Account(
                    r["account_id"],
                    r["user_id"],
                    r["account_type"],
                    r["balance"],
                    r["created_at"],
                )
                for r in cur.fetchall()
            ]

    def get_balance(self, account_id: int):
        with get_cursor() as cur:
            cur.execute(
                "SELECT balance FROM accounts WHERE account_id = ?",
                (account_id,),
            )
            row = cur.fetchone()
            return row["balance"] if row else None