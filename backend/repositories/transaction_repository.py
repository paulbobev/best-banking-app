# repositories/transaction_repository.py
from decimal import Decimal
from db import _connect, get_cursor
from models.transaction_entity import Transaction


class TransactionRepository:

    def deposit(self, account_id: int, amount: Decimal, txn_type="DEPOSIT") -> int:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        conn = _connect()
        try:
            conn.execute("BEGIN IMMEDIATE")     # write lock before touching balances
            row = conn.execute(
                "SELECT balance FROM accounts WHERE account_id = ?",
                (account_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"Account {account_id} not found")
            new_balance = Decimal(row["balance"]) + amount
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE account_id = ?",
                (str(new_balance), account_id),
            )
            cur = conn.execute(
                "INSERT INTO transactions (account_id, txn_type, amount) VALUES (?, ?, ?)",
                (account_id, txn_type, amount),
            )
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def withdraw(self, account_id: int, amount: Decimal,txn_type="WITHDRAW") -> int:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        conn = _connect()
        try:
            conn.execute("BEGIN IMMEDIATE")     # lock BEFORE the balance check
            row = conn.execute(
                "SELECT balance FROM accounts WHERE account_id = ?",
                (account_id,),
            ).fetchone()
            if row is None:
                raise ValueError(f"Account {account_id} not found")
            balance = Decimal(row["balance"])
            if balance < amount:
                raise ValueError("Insufficient funds")
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE account_id = ?",
                (str(balance - amount), account_id),
            )
            cur = conn.execute(
                "INSERT INTO transactions (account_id, txn_type, amount) VALUES (?, ?, ?)",
                (account_id, txn_type, amount),
            )
            conn.commit()
            return cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def transfer(self, from_account_id: int, to_account_id: int, amount: Decimal) -> tuple[int, int]:
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        if from_account_id == to_account_id:
            raise ValueError("Cannot transfer to the same account")

        conn = _connect()
        try:
            conn.execute("BEGIN IMMEDIATE")     # lock before reading either balance

            from_row = conn.execute(
                "SELECT balance FROM accounts WHERE account_id = ?",
                (from_account_id,),
            ).fetchone()
            if from_row is None:
                raise ValueError(f"Account {from_account_id} not found")

            to_row = conn.execute(
                "SELECT balance FROM accounts WHERE account_id = ?",
                (to_account_id,),
            ).fetchone()
            if to_row is None:
                raise ValueError(f"Account {to_account_id} not found")

            from_balance = Decimal(from_row["balance"])
            if from_balance < amount:
                raise ValueError("Insufficient funds")

            to_balance = Decimal(to_row["balance"])

            # Debit sender
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE account_id = ?",
                (str(from_balance - amount), from_account_id),
            )
            out_cur = conn.execute(
                "INSERT INTO transactions (account_id, txn_type, amount) VALUES (?, ?, ?)",
                (from_account_id, "TRANSFEROUT", amount),
            )

            # Credit receiver
            conn.execute(
                "UPDATE accounts SET balance = ? WHERE account_id = ?",
                (str(to_balance + amount), to_account_id),
            )
            in_cur = conn.execute(
                "INSERT INTO transactions (account_id, txn_type, amount) VALUES (?, ?, ?)",
                (to_account_id, "TRANSFERIN", amount),
            )

            conn.commit()
            return out_cur.lastrowid, in_cur.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def find_by_id(self, txn_id: int):
        with get_cursor() as cur:
            cur.execute(
                "SELECT txn_id, account_id, txn_type, amount, created_at "
                "FROM transactions WHERE txn_id = ?",
                (txn_id,),
            )
            r = cur.fetchone()
            if r is None:
                return None
            return Transaction(r["txn_id"], r["account_id"], r["txn_type"], r["amount"], r["created_at"])

    def find_by_account(self, account_id: int):
        with get_cursor() as cur:
            cur.execute(
                "SELECT txn_id, account_id, txn_type, amount, created_at "
                "FROM transactions WHERE account_id = ? "
                "ORDER BY created_at DESC, txn_id DESC",
                (account_id,),
            )
            return [
                Transaction(r["txn_id"], r["account_id"], r["txn_type"], r["amount"], r["created_at"])
                for r in cur.fetchall()
            ]