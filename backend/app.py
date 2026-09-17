from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.auth import router as auth_router, require_roles


# Domain Entities
from models.account_entity import Account, CheckingAccount, SavingsAccount
# Request / Response Schemas
from models.schemas import (
    AccountCreate,
    AccountResponse,
    AmountPayload,
    BalanceResponse,
    TransactionResponse,
    TransferRequest,
    TransferResponse,
    UserCreate,
    UserResponse,
)
from models.transaction_entity import Transaction
from models.user_entity import User
from repositories.account_repository import AccountRepository
from repositories.user_repository import UserRepository
import services.transaction_service as transaction_service

app = FastAPI(title="Simple Bank Application API (Object-Oriented)")

user_repo = UserRepository()
account_repo = AccountRepository()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- User Registration Route ---


@app.post("/api/users", response_model=UserResponse)
def create_user(data: UserCreate):
    if user_repo.find_by_email(data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = user_repo.create(data.name, data.email)
    return {"userId": user_id, "name": data.name, "email": data.email}


# --- Account Routes ---


@app.post("/api/accounts", response_model=AccountResponse)
def create_account(data: AccountCreate):
    user = user_repo.find_by_id(data.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User ID does not exist")

    account_id = account_repo.create(
        user_id=data.userId,
        account_type=data.accountType.upper(),
        initial_balance=Decimal("0.00"),
    )
    created_account = account_repo.find_by_id(account_id)
    if not created_account:
        raise HTTPException(status_code=500, detail="Failed to retrieve created account")

    return {
        "accountId": created_account.account_id,
        "userName": user.name,
        "balance": created_account.balance,
        "accountType": created_account.account_type,
    }


@app.get("/api/users/{name}/accounts", response_model=List[AccountResponse])
def get_user_accounts(name: str):
    matched_user = user_repo.find_by_name(name)
    if not matched_user:
        raise HTTPException(status_code=404, detail="User not found")

    accounts = account_repo.find_by_user(matched_user.user_id)
    return [
        {
            "accountId": acc.account_id,
            "userName": matched_user.name,
            "balance": acc.balance,
            "accountType": acc.account_type,
        }
        for acc in accounts
    ]


@app.get("/api/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int):
    account = account_repo.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    user = user_repo.find_by_id(account.user_id)
    return {
        "accountId": account.account_id,
        "userName": user.name if user else "Unknown",
        "balance": account.balance,
        "accountType": account.account_type,
    }
    
@app.get("/api/accounts", response_model=List[AccountResponse])
def get_all_accounts():
    accounts = account_repo.find_all()

    result = []
    for acc in accounts:
        user = user_repo.find_by_id(acc.user_id)
        result.append({
            "accountId": acc.account_id,
            "userName": user.name if user else "Unknown",
            "balance": acc.balance,
            "accountType": acc.account_type,
        })

    return result


# --- Transaction Routes ---


@app.post("/api/accounts/{account_id}/deposit", response_model=BalanceResponse)
def deposit(account_id: int, data: AmountPayload):
    try:
        transaction_service.deposit(account_id, data.amount)
        current_balance = transaction_service.balance_check(account_id)
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))

    return {"accountId": account_id, "balance": current_balance}


@app.post("/api/accounts/{account_id}/withdraw", response_model=BalanceResponse)
def withdraw(account_id: int, data: AmountPayload):
    try:
        transaction_service.withdraw(account_id, data.amount)
        current_balance = transaction_service.balance_check(account_id)
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))

    return {"accountId": account_id, "balance": current_balance}


@app.post("/api/accounts/{account_id}/transfer", response_model=TransferResponse)
def transfer(account_id: int, data: TransferRequest):
    try:
        transaction_service.transfer(account_id, data.toAccountId, data.amount)
        source_balance = transaction_service.balance_check(account_id)
        target_balance = transaction_service.balance_check(data.toAccountId)
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        raise HTTPException(status_code=status_code, detail=str(e))

    return {
        "message": "Transfer successful",
        "sourceAccountId": account_id,
        "sourceBalance": source_balance,
        "targetAccountId": data.toAccountId,
        "targetBalance": target_balance,
    }


@app.get(
    "/api/accounts/{account_id}/transactions",
    response_model=List[TransactionResponse],
)
def get_transactions(account_id: int):
    account = account_repo.find_by_id(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    history = transaction_service.transaction_history(account_id)
    return [
        {"type": t.txn_type, "amount": t.amount, "date": t.created_at}
        for t in history
    ]
