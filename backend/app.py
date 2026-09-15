from db import init_db
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from models.account_entity import Account, CheckingAccount, SavingsAccount
from models.transaction_entity import Transaction
from models.user_entity import User

app = FastAPI(title="Simple Bank Application API (Object-Oriented)")

init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage using class instances
user_id_counter = 1
account_id_counter = 1
txn_id_counter = 1

users_db: Dict[int, User] = {}
accounts_db: Dict[int, Account] = {}
transactions_db: List[Transaction] = []


# Pydantic Schemas
class AccountCreateRequest(BaseModel):
  account_id: Optional[int] = None
  name: str
  email: str
  accountType: str

  model_config = {
      "json_schema_extra": {
          "example": {
              "name": "John Doe",
              "email": "john.doe@example.com",
              "accountType": "Savings",
          }
      }
  }


class AmountRequest(BaseModel):
  amount: Decimal

  model_config = {"json_schema_extra": {"example": {"amount": 100.0}}}


# -------------------------------------------------------------------
# REST API Endpoints (Name-Based & Entity Model Integrated)
# -------------------------------------------------------------------


# 1. List All Accounts (GET /api/accounts)
@app.get("/api/accounts")
def get_all_accounts():
  account_list = []
  for account in accounts_db.values():
    user = users_db.get(account.user_id)
    account_list.append({
        "userName": user.name if user else "Unknown",
        "email": user.email if user else "Unknown",
        "balance": float(account.getBalance()),
        "accountType": account.account_type,
    })
  return account_list


# 2. Create Account (POST /api/accounts)
@app.post("/api/accounts")
def create_account(data: AccountCreateRequest):
  global user_id_counter, account_id_counter

  # Check if user already exists by name or email
  existing_user = None
  for user in users_db.values():
    if user.name.strip().lower() == data.name.strip().lower():
      existing_user = user
      break

  if existing_user is None:
    for user in users_db.values():
      if user.email == data.email:
        existing_user = user
        break

  if existing_user is None:
    user = User(
        user_id=user_id_counter, name=data.name, email=data.email
    ) [cite: 6]
    users_db[user_id_counter] = user
    user_id_counter += 1
  else:
    user = existing_user

  # Instantiate subclass based on accountType
  acc_type_upper = data.accountType.upper()
  created_at_str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

  if acc_type_upper == "SAVINGS":
    account = SavingsAccount(
        account_id=account_id_counter,
        user_id=user.user_id,
        balance=Decimal("0.00"),
        created_at=created_at_str,
    ) [cite: 4]
  elif acc_type_upper == "CHECKING":
    account = CheckingAccount(
        account_id=account_id_counter,
        user_id=user.user_id,
        balance=Decimal("0.00"),
        created_at=created_at_str,
    ) [cite: 4]
  else:
    account = Account(
        account_id=account_id_counter,
        user_id=user.user_id,
        account_type=data.accountType,
        balance=Decimal("0.00"),
        created_at=created_at_str,
    ) [cite: 4]

  accounts_db[account_id_counter] = account
  account_id_counter += 1

  return {
      "userName": user.name,
      "email": user.email,
      "balance": float(account.getBalance()),
      "accountType": account.account_type,
  }


# 3. Get Account Details by Name (GET /api/accounts/user/{name})
@app.get("/api/accounts/user/{name}")
def get_account_by_name(name: str):
  user = None
  for u in users_db.values():
    if u.name.strip().lower() == name.strip().lower():
      user = u
      break

  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  account = None
  for acc in accounts_db.values():
    if acc.user_id == user.user_id:
      account = acc
      break

  if not account:
    raise HTTPException(
        status_code=404, detail="No account found for this user"
    )

  return {
      "userName": user.name,
      "email": user.email,
      "balance": float(account.getBalance()),
      "accountType": account.account_type,
  }


# 4. Deposit Money by Name (POST /api/accounts/user/{name}/deposit)
@app.post("/api/accounts/user/{name}/deposit")
def deposit_by_name(name: str, data: AmountRequest):
  global txn_id_counter

  user = None
  for u in users_db.values():
    if u.name.strip().lower() == name.strip().lower():
      user = u
      break

  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  account = None
  for acc in accounts_db.values():
    if acc.user_id == user.user_id:
      account = acc
      break

  if not account:
    raise HTTPException(
        status_code=404, detail="No account found for this user"
    )

  try:
    new_balance = account.deposit(data.amount) [cite: 4]
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

  txn = Transaction(
      txn_id=txn_id_counter,
      account_id=account.account_id,
      txn_type="DEPOSIT",
      amount=data.amount,
      created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  ) [cite: 5]
  transactions_db.append(txn)
  txn_id_counter += 1

  return {
      "message": f"Deposit successful for {user.name}",
      "newBalance": float(new_balance),
  }


# 5. Withdraw Money by Name (POST /api/accounts/user/{name}/withdraw)
@app.post("/api/accounts/user/{name}/withdraw")
def withdraw_by_name(name: str, data: AmountRequest):
  global txn_id_counter

  user = None
  for u in users_db.values():
    if u.name.strip().lower() == name.strip().lower():
      user = u
      break

  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  account = None
  for acc in accounts_db.values():
    if acc.user_id == user.user_id:
      account = acc
      break

  if not account:
    raise HTTPException(
        status_code=404, detail="No account found for this user"
    )

  try:
    new_balance = account.withdraw(data.amount) [cite: 4]
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

  txn = Transaction(
      txn_id=txn_id_counter,
      account_id=account.account_id,
      txn_type="WITHDRAW",
      amount=data.amount,
      created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
  ) [cite: 5]
  transactions_db.append(txn)
  txn_id_counter += 1

  return {
      "message": f"Withdrawal successful for {user.name}",
      "newBalance": float(new_balance),
  }


# 6. View Transaction History by Name (GET /api/accounts/user/{name}/transactions)
@app.get("/api/accounts/user/{name}/transactions")
def get_transactions_by_name(name: str):
  user = None
  for u in users_db.values():
    if u.name.strip().lower() == name.strip().lower():
      user = u
      break

  if not user:
    raise HTTPException(status_code=404, detail="User not found")

  account = None
  for acc in accounts_db.values():
    if acc.user_id == user.user_id:
      account = acc
      break

  if not account:
    raise HTTPException(
        status_code=404, detail="No account found for this user"
    )

  account_txns = [
      {
          "type": t.txn_type,
          "amount": float(t.amount),
          "date": t.created_at,
      }
      for t in transactions_db
      if t.account_id == account.account_id
  ]

  return account_txns