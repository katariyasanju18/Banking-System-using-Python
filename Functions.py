from Database import *
from datetime import datetime

# Function to show balance
def show_balance(account_number):
    cursor.execute("SELECT initial_balance FROM customers WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    if result:
        print(f"Your balance is: {result[0]}")
    else:
        print("Account not found.")

# Function to show transaction history
def show_transaction(account_number):
    cursor.execute("SELECT * FROM transaction WHERE account_number = %s", (account_number,))
    transactions = cursor.fetchall()
    if transactions:
        for txn in transactions:
            print(f"Transaction ID: {txn[0]}, Type: {txn[2]}, Amount: {txn[3]}, Date: {txn[4]}")
    else:
        print("No transactions found for this account.")

# Function to credit amount
def credit_amount(account_number, amount):
    # Validate that the amount is a positive number and is not too large
    if not isinstance(amount, (int, float)) or amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return
    
    # Ensure amount is properly formatted as a decimal
    amount = round(amount, 2)

    # Execute the query to insert the transaction
    cursor.execute("INSERT INTO transaction (account_number, transaction_type, amount) VALUES (%s, 'credit', %s)", (account_number, amount))
    mydb.commit()

    # Update balance after the credit transaction
    cursor.execute("UPDATE customers SET initial_balance = initial_balance + %s WHERE account_number = %s", (amount, account_number))
    mydb.commit()

    print(f"Amount {amount} credited successfully to account {account_number}.")

# Function to debit amount
def debit_amount(account_number, amount):
    cursor.execute("SELECT initial_balance FROM customers WHERE account_number = %s", (account_number,))
    result = cursor.fetchone()
    
    if result and result[0] >= amount:
        cursor.execute("UPDATE customers SET initial_balance = initial_balance - %s WHERE account_number = %s", (amount, account_number))
        mydb.commit()

        cursor.execute("INSERT INTO transaction (account_number, transaction_type, amount) VALUES (%s, 'debit', %s)", (account_number, amount))
        mydb.commit()

        print(f"{amount} debited successfully from account {account_number}.")
    else:
        print("Insufficient balance or account not found.")

# Function to transfer amount
def transfer_amount(from_account, to_account, amount):
    # Validate the transfer amount
    if amount <= 0:
        print("Amount should be greater than 0.")
        return

    # Check if the sender has sufficient balance
    cursor.execute("SELECT initial_balance FROM customers WHERE account_number = %s", (from_account,))
    sender_balance = cursor.fetchone()
    if not sender_balance or sender_balance[0] < amount:
        print("Insufficient balance for transfer.")
        return
    
    # Check if the recipient account exists
    cursor.execute("SELECT initial_balance FROM customers WHERE account_number = %s", (to_account,))
    recipient_balance = cursor.fetchone()
    if not recipient_balance:
        print("Recipient account not found.")
        return

    # Perform the transfer (update the sender and receiver balances)
    try:
        # Begin a transaction
        cursor.execute("START TRANSACTION;")
        
        cursor.execute("UPDATE customers SET initial_balance = initial_balance - %s WHERE account_number = %s", (amount, from_account))
        cursor.execute("UPDATE customers SET initial_balance = initial_balance + %s WHERE account_number = %s", (amount, to_account))

        # Insert transaction records for both accounts
        cursor.execute("INSERT INTO transaction (account_number, transaction_type, amount, to_account_number) VALUES (%s, 'debit', %s, %s)", (from_account, amount, to_account))
        cursor.execute("INSERT INTO transaction (account_number, transaction_type, amount, to_account_number) VALUES (%s, 'credit', %s, %s)", (to_account, amount, from_account))

        mydb.commit()
        print(f"Transferred {amount} from {from_account} to {to_account}.")
    except Exception as e:
        mydb.rollback()  # In case of error, rollback the transaction
        print("Transaction failed. Rolled back changes.")
        print(str(e))

# Function to delete account
def delete_account(account_number):
    # First, delete the related transactions
    cursor.execute("DELETE FROM transaction WHERE account_number = %s", (account_number,))
    
    # Then, delete the related login record
    cursor.execute("DELETE FROM login WHERE account_number = %s", (account_number,))
    
    # Then, delete the customer record
    cursor.execute("DELETE FROM customers WHERE account_number = %s", (account_number,))
    
    mydb.commit()
    print(f"Account {account_number}, related transactions, and login record deleted successfully.")

# Function to change password
def change_password(account_number, new_password):
    cursor.execute("UPDATE login SET password = %s WHERE account_number = %s", (new_password, account_number))
    mydb.commit()
    print("Password updated successfully.")

# Function to update profile
def update_profile(account_number, name=None, city=None, contact_number=None, email_id=None, address=None):
    if name:
        cursor.execute("UPDATE customers SET name = %s WHERE account_number = %s", (name, account_number))
    if city:
        cursor.execute("UPDATE customers SET city = %s WHERE account_number = %s", (city, account_number))
    if contact_number:
        cursor.execute("UPDATE customers SET contact_number = %s WHERE account_number = %s", (contact_number, account_number))
    if email_id:
        cursor.execute("UPDATE customers SET email_id = %s WHERE account_number = %s", (email_id, account_number))
    if address:
        cursor.execute("UPDATE customers SET address = %s WHERE account_number = %s", (address, account_number))
    
    mydb.commit()
    print(f"Profile updated successfully for account {account_number}.")