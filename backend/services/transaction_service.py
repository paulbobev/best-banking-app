from repositories import account_repository
from repositories.transaction_repository import TransactionRepository
from decimal import Decimal

transaction_repository = TransactionRepository()
def transfer(from_account_id, to_account_id, amount: Decimal):

    #Recieving objects from repository
    from_account = account_repository.get_account(from_account_id)
    to_account = account_repository.get_account(to_account_id)

    #To check if the account exhist and we can transfer funds
    if to_account is None:
        raise ValueError("Account Receiver ID not found")
    if from_account is None: 
        raise ValueError("Account Sender ID not found") 
    if from_account_id == to_account_id:
        raise ValueError("Cannot transfer to the same account.")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    if from_account.balance < amount:
        raise ValueError("Insufficient funds.")
    #Transfering the funds
    transaction_repository.withdraw(from_account_id, amount,"TRANSFEROUT")
    transaction_repository.deposit(to_account_id, amount,"TRANSFERIN")
    
    #returning the new balances
    from_account = account_repository.get_account(from_account_id)
    to_account = account_repository.get_account(to_account_id)
    return from_account.balance, to_account.balance


#Checks if account is valid and returns accounts balance
def balance_check(account_id):
    #Recieving objects from repository
    account = account_repository.get_account(account_id)
    #To check if the account exhist
    if account is None:
        raise ValueError("Account ID not found")
    return account.balance 

# Validates account and amount then will execute the deposit. Returns a string with a message
def deposit(account_id, amount):
    return transaction_repository.deposit(account_id, amount)
   

# Validates account and amount then will execute the withdraw. Returns a string with a message
def withdraw(account_id, amount):
    return transaction_repository.withdraw(account_id, amount)
    

#Should just recieve a list of a accounts transaction history
def transaction_history(account_id):
    return transaction_repository.find_by_account(account_id)
    


    
