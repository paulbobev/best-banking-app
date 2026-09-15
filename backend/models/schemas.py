# Schemas.py is utilized for the JSON responses

# Pydantic is utilized within FastAPI so I will be using this
# BaseModel is the foundation for the data structure and validation
# Emailstr validated proper emails
# Field ensures proper constraints within fields
from pydantic import BaseModel, EmailStr, Field

# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# User Schemas

class UserCreate(BaseModel):
    name: str = Field(min_length = 1)
    email: EmailStr

class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str

# Account Schemas

class AccountCreate(BaseModel):
    userId: int
    accountType: str

class AccountResponse(BaseModel):
    accountId: int
    userName: str
    balance: Decimal

class AccountCreatedResponse(BaseModel):
    accountId: int
    accountType: str

# Transaction Schemas

class AmountPayload(BaseModel):
    # gt=0 means that the amount must be above 0
    amount: Decimal = Field(gt=0, description="Amount must be positive")

class BalanceResponse(BaseModel):
    accountId: int
    balance: float

class TransactionResponse(BaseModel):
    type: str
    amount: Decimal
    date: str

class TransferRequest(BaseModel):
    toAccountId: int
    # gt=0 means that the amount must be above 0
    amount: Decimal = Field(gt=0, description="Amount must be positive")

class TransferResponse(BaseModel):
    message: str
    sourceAccountId: int
    sourceBalance: Decimal
    targetAccoundId: int

