from datetime import datetime
from decimal import Decimal
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

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

app = FastAPI(title="Simple Bank Application API (Object-Oriented)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
user_id_counter = 1
account_id_counter = 1
txn_id_counter = 1

users_db: Dict[int, User] = {}
accounts_db: Dict[int, Account] = {}
transactions_db: List[Transaction] = []


# --- Helper Lookup Functions ---


def find_user_by_name(name: str) -> User | None:
    for user in users_db.values():
        if user.name.strip().lower() == name.strip().lower():
            return user
        return None


# --- User Registration Route ---


@app.post("/api/users", response_model=UserResponse)
def create_user(data: UserCreate):
    global user_id_counter

    for u in users_db.values():
        if u.email.lower() == data.email.lower():
            raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        user_id=user_id_counter,
        name=data.name,
        email=data.email,
        created_at=datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
    )
    users_db[user_id_counter] = user
    user_id_counter += 1

    return {"userId": user.user_id, "name": user.name, "email": user.email}


# --- Account Routes ---


@app.get("/api/accounts", response_model=List[AccountResponse])
def get_all_accounts():
    account_list = []
    for account in accounts_db.values():
        user = users_db.get(account.user_id)
        account_list.append(
            {
                "accountId": account.account_id,
                "userName": user.name if user else "Unknown",
                "email": user.email if user else "Unknown",
                "balance": account.getBalance(),
                "accountType": account.account_type,
            }
        )
    return account_list


@app.post("/api/accounts", response_model=AccountResponse)
def create_account(data: AccountCreate):
    global account_id_counter

    user = users_db.get(data.userId)
    if not user:
        raise HTTPException(status_code=404, detail="User ID does not exist")

    acc_type_upper = data.accountType.upper()
    created_at_str = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    if acc_type_upper == "SAVINGS":
        account = SavingsAccount(
            account_id=account_id_counter,
            user_id=user.user_id,
            balance=Decimal("0.00"),
            created_at=created_at_str,
        )
    elif acc_type_upper == "CHECKING":
        account = CheckingAccount(
            account_id=account_id_counter,
            user_id=user.user_id,
            balance=Decimal("0.00"),
            created_at=created_at_str,
        )
    else:
        account = Account(
            account_id=account_id_counter,
            user_id=user.user_id,
            account_type=data.accountType,
            balance=Decimal("0.00"),
            created_at=created_at_str,
        )

    accounts_db[account_id_counter] = account
    account_id_counter += 1

    return {
        "accountId": account.account_id,
        "userName": user.name,
        "email": user.email,
        "balance": account.getBalance(),
        "accountType": account.account_type,
    }


@app.get("/api/users/{name}/accounts", response_model=List[AccountResponse])
def get_user_accounts(name: str):
    user = find_user_by_name(name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_accounts = []
    for acc in accounts_db.values():
        if acc.user_id == user.user_id:
            user_accounts.append(
                {
                    "accountId": acc.account_id,
                    "userName": user.name,
                    "email": user.email,
                    "balance": acc.getBalance(),
                    "accountType": acc.account_type,
                }
            )

    return user_accounts


@app.get("/api/accounts/{account_id}", response_model=AccountResponse)
def get_account(account_id: int):
    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    user = users_db.get(account.user_id)
    return {
        "accountId": account.account_id,
        "userName": user.name if user else "Unknown",
        "email": user.email if user else "Unknown",
        "balance": account.getBalance(),
        "accountType": account.account_type,
    }


# --- Transaction Routes ---


@app.post("/api/accounts/{account_id}/deposit", response_model=BalanceResponse)
def deposit(account_id: int, data: AmountPayload):
    global txn_id_counter

    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    try:
        new_balance = account.deposit(data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    transactions_db.append(
        Transaction(
            txn_id=txn_id_counter,
            account_id=account.account_id,
            txn_type="DEPOSIT",
            amount=data.amount,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    )
    txn_id_counter += 1

    return {"accountId": account.account_id, "balance": new_balance}


@app.post("/api/accounts/{account_id}/withdraw", response_model=BalanceResponse)
def withdraw(account_id: int, data: AmountPayload):
    global txn_id_counter

    account = accounts_db.get(account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    try:
        new_balance = account.withdraw(data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    transactions_db.append(
        Transaction(
            txn_id=txn_id_counter,
            account_id=account.account_id,
            txn_type="WITHDRAW",
            amount=data.amount,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
    )
    txn_id_counter += 1

    return {"accountId": account.account_id, "balance": new_balance}


@app.post("/api/accounts/{account_id}/transfer", response_model=TransferResponse)
def transfer(account_id: int, data: TransferRequest):
    global txn_id_counter

    source_acc = accounts_db.get(account_id)
    target_acc = accounts_db.get(data.toAccountId)

    if not source_acc:
        raise HTTPException(status_code=404, detail="Source account not found")
    if not target_acc:
        raise HTTPException(status_code=404, detail="Target account not found")
    if source_acc.account_id == target_acc.account_id:
        raise HTTPException(
            status_code=400, detail="Cannot transfer funds to the same account"
        )

    try:
        source_acc.withdraw(data.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    target_acc.deposit(data.amount)

    source_user = users_db.get(source_acc.user_id)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    transactions_db.extend(
        [
            Transaction(
                txn_id=txn_id_counter,
                account_id=source_acc.account_id,
                txn_type="TRANSFER_OUT",
                amount=data.amount,
                created_at=timestamp,
            ),
            Transaction(
                txn_id=txn_id_counter + 1,
                account_id=target_acc.account_id,
                txn_type="TRANSFER_IN",
                amount=data.amount,
                created_at=timestamp,
            ),
        ]
    )
    txn_id_counter += 2

    return {
        "message": "Transfer successful",
        "sourceAccountId": source_acc.account_id,
        "sourceUserName": source_user.name if source_user else "Unknown",
        "sourceBalance": source_acc.getBalance(),
        "targetAccountId": target_acc.account_id,
        "targetBalance": target_acc.getBalance(),
    }


@app.get(
    "/api/accounts/{account_id}/transactions",
    response_model=List[TransactionResponse],
)
def get_transactions(account_id: int):
    if account_id not in accounts_db:
        raise HTTPException(status_code=404, detail="Account not found")

    return [
        {"type": t.txn_type, "amount": t.amount, "date": t.created_at}
        for t in transactions_db
        if t.account_id == account_id
    ]
