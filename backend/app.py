from datetime import datetime
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Simple Bank Application API (In-Memory)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


user_id_counter = 1
account_id_counter = 1
txn_id_counter = 1

users_db = {}
accounts_db = ({})
transactions_db = ([])


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
                "accountType": "Savings"
            }
        }
    }


class AmountRequest(BaseModel):
    amount: float

    model_config = {
        "json_schema_extra": {
            "example": {
                "amount": 100.0
            }
        }
    }


@app.get("/api/accounts")
def get_all_accounts():
  account_list = []
  for account_id, account_info in accounts_db.items():
    user = users_db.get(account_info["user_id"], {})
    account_list.append({
        "accountId": account_id,
        "userName": user.get("name", "Unknown"),
        "balance": account_info["balance"],
        "accountType": account_info["account_type"],
    })
  return account_list

@app.post("/api/accounts")
def create_account(data: AccountCreateRequest):
    global user_id_counter, account_id_counter

    existing_user_id = None
    for uid, user_info in users_db.items():
        if user_info["email"] == data.email:
            existing_user_id = uid
            break

    if existing_user_id is None:
        user_id = user_id_counter
        users_db[user_id] = {"name": data.name, "email": data.email}
        user_id_counter += 1
    else:
        user_id = existing_user_id

    account_id = account_id_counter
    accounts_db[account_id] = {
        "user_id": user_id,
        "balance": 0.0,
        "account_type": data.accountType,
    }
    account_id_counter += 1

    return {
        "accountId": account_id,
        "userName": users_db[user_id]["name"],
        "balance": accounts_db[account_id]["balance"],
    }  #


@app.get("/api/accounts/{account_id}")
def get_account(account_id: int):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")

    account = accounts_db[account_id]
    user = users_db[account["user_id"]]

    return {
        "accountId": account_id,
        "userName": user["name"],
        "balance": account["balance"],
    }  #[cite: 1]


@app.post("/api/accounts/{account_id}/deposit")
def deposit(account_id: int, data: AmountRequest):
    global txn_id_counter

    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")

    # Business Rule: Deposit amount must be positive
    if data.amount <= 0:
        raise HTTPException(
            status_code=400, detail="Deposit amount must be positive"
        )  #[cite: 1]

    accounts_db[account_id]["balance"] += data.amount

    txn_record = {
        "txn_id": txn_id_counter,
        "account_id": account_id,
        "txn_type": "DEPOSIT",
        "amount": data.amount,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    transactions_db.append(txn_record)
    txn_id_counter += 1

    return {
        "message": "Deposit successful",
        "newBalance": accounts_db[account_id]["balance"],
    }


@app.post("/api/accounts/{account_id}/withdraw")
def withdraw(account_id: int, data: AmountRequest):
    global txn_id_counter

    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")

    if data.amount <= 0:
        raise HTTPException(
            status_code=400, detail="Withdrawal amount must be positive"
        )

    current_balance = accounts_db[account_id]["balance"]
    if current_balance < data.amount:
        raise HTTPException(
            status_code=400, detail="Insufficient balance"
        )  #[cite: 1]

    accounts_db[account_id]["balance"] -= data.amount

    txn_record = {
        "txn_id": txn_id_counter,
        "account_id": account_id,
        "txn_type": "WITHDRAW",
        "amount": data.amount,
        "date": datetime.now().strftime("%Y-%m-%d"),
    }
    transactions_db.append(txn_record)
    txn_id_counter += 1

    return {
        "message": "Withdrawal successful",
        "newBalance": accounts_db[account_id]["balance"],
    }


@app.get("/api/accounts/{account_id}/transactions")
def get_transactions(account_id: int):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")

    account_txns = [
        {"type": t["txn_type"], "amount": t["amount"], "date": t["date"]}
        for t in transactions_db
        if t["account_id"] == account_id
    ]

    return account_txns

