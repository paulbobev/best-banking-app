# models/account_entity.py
# Using decimal in order to keep transactions precise (floats can have some odd interactions)
from decimal import Decimal

# Parent Class: Contains shared attributes and base behavior.
class Account:

# init here to assign values
  def __init__(self, account_id: int, user_id: int, account_type: str, balance: Decimal):
    self.account_id = account_id
    self.user_id = user_id
    self.account_type = account_type
    self.balance = balance

# Deposits money to the account
  def deposit(self, amount: Decimal) -> Decimal:
    # Decimal value that must be positive according to business rules
    if amount <= 0:
      raise ValueError("Deposit amount must be positive")
    self.balance += amount
    return self.balance

# Withdraws money from the account
  def withdraw(self, amount: Decimal) -> Decimal:
    # Prevent negative withdrawals (giving yourself money)
    if amount <= 0:
      raise ValueError("Withdrawal amount must be positive")
    # Cannot withdraw more than current balance according to business rules
    if amount > self.balance:
      raise ValueError("Cannot withdraw more than balance")
    
    self.balance -= amount
    return self.balance


# Child classes for future functionality and naming the accounts
class SavingsAccount(Account):
  def __init__(self, account_id: int, user_id: int, balance: Decimal):

    # Super init calls init constructor from the parent class so it can initalize with the given values
    super().__init__(account_id, user_id, "SAVINGS", balance)


class CheckingAccount(Account):
  """Child Class: Implements overdraft capability."""

  def __init__(self, account_id: int, user_id: int, balance: Decimal):
    # Super init calls init constructor from the parent class so it can initalize with the given values
    super().__init__(account_id, user_id, "CHECKING", balance)
