# Schemas.py is utilized for formatting JSON responses and defining validation rules for API requests

# Pydantic is utilized within FastAPI so I will be using this
# BaseModel is the foundation for the data structure and validation
# Emailstr validated proper emails
# Field ensures proper constraints within fields
from pydantic import BaseModel, EmailStr, Field

# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# User Schemas

# Validates incoming data when creating a user
class UserCreate(BaseModel):
    name: str = Field(min_length = 1)
    email: EmailStr

# Formats the response returned after fetching or creating a user
class UserResponse(BaseModel):
    userId: int
    name: str
    email: str

# Account Schemas

# Validates incoming data when creating an account
class AccountCreate(BaseModel):
    userId: int
    accountType: str

# Formats the response returned after fetching an account
class AccountResponse(BaseModel):
    accountId: int
    userName: str
    balance: Decimal

# Formats the response returned after creating an account
class AccountCreatedResponse(BaseModel):
    accountId: int
    accountType: str

# Transaction Schemas

# Validates incoming data for operations such as withdrawals and deposits
class AmountPayload(BaseModel):
    # gt=0 means that the amount must be above 0
    amount: Decimal = Field(gt=0, description="Amount must be positive")

# Formats response for showing an account's balance
class BalanceResponse(BaseModel):
    accountId: int
    balance: Decimal

# Formats details for transaction history
class TransactionResponse(BaseModel):
    type: str
    amount: Decimal
    date: str

# Validates incoming data when transferring funds to another account
class TransferRequest(BaseModel):
    toAccountId: int
    # gt=0 means that the amount must be above 0
    amount: Decimal = Field(gt=0, description="Amount must be positive")

# Formats the response after a successful transfer
class TransferResponse(BaseModel):
    message: str
    sourceAccountId: int
    sourceBalance: Decimal
    targetAccountId: int

