#USER REGISTRATION SIGNIN AND SIGNUP
from Database import *
from random import randint
from Customer import *
from datetime import datetime
from Functions import*
# MENU AFTER LOGIN
def allcalls(account_number):
    while True:
        Menu = '''
              MENU
          1.SHOW BALANCE
          2.SHOW TRANSACTION
          3.CREDIT AMOUNT
          4.DEBIT AMOUNT
          5.TRANFER AMOUNT
          6.DELETE THE ACCOUNT
          7.CHANGE PASSWORD
          8.UPDATE PROFILE
          9.LOGOUT
          '''
        print("Welcome To The Bank")
        print(Menu)
        choice = int(input("Enter Your Choice:"))
        if choice == 1:
            show_balance(account_number)
        elif choice == 2:
            show_transaction(account_number)
        elif choice == 3:
            amount = float(input("Enter amount to credit: "))
            credit_amount(account_number, amount)
        elif choice == 4:
            amount = float(input("Enter amount to debit: "))
            debit_amount(account_number, amount)
        elif choice == 5:
            to_account = input("Enter recipient account number: ")
            amount = float(input("Enter amount to transfer: "))
            transfer_amount(account_number, to_account, amount)
        elif choice == 6:
            delete_account(account_number)
            break 
        elif choice == 7:
            new_password = input("Enter new password: ")
            change_password(account_number, new_password)
        elif choice == 8:
            print("Update Profile: (Leave blank to keep unchanged)")
            name = input("Enter new name: ")
            city = input("Enter new city: ")
            contact_number = input("Enter new contact number: ")
            email_id = input("Enter new email: ")
            address = input("Enter new address: ")
            update_profile(account_number, name, city, contact_number, email_id, address)
        elif choice == 9:
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please choose between 1 and 9.")
            
#SIGNUP PAGE
def Signup():
    P_username = input("Create Username: ")
    temp = db_query(f"SELECT username FROM customers WHERE username = '{P_username}';")
    if temp:
        print("Username already exists. Please try another.")
        Signup()
    else:
        print("Username is available. Please proceed.")
        
        # Password Validation
        while True:
            password = input("Enter Your Password: ")
            if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isupper() for char in password) or not any(char in '!@#$%^&*()_+' for char in password):
                print("Password is not strong enough. It should be at least 8 characters long, contain an uppercase letter, a number, and a special character.")
                continue
            else:
                break

        name = input("Enter Your Name: ")
        
        # DOB Validation (Format: YYYY-MM-DD)
        while True:
            dob = input("Enter Your Date of Birth (YYYY-MM-DD): ")
            try:
                dob_date = datetime.strptime(dob, "%Y-%m-%d")
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        age = input("Enter Your Age: ")
        city = input("Enter Your City: ")
        
        # Account Number Generation
        while True:
            account_number = randint(1000000000, 9999999999)
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if not temp:
                break
        print("Account number generated:", account_number)

        initial_balance = 2000
        
        # Contact Number Validation
        while True:
            contact_number = input("Enter Your Contact Number: ")
            if len(contact_number) != 10 or not contact_number.isdigit():
                print("Invalid contact number. It should be exactly 10 digits.")
                continue
            else:
                break

        # Email Validation
        while True:
            email = input("Enter Your Email ID: ")
            if "@" not in email or "." not in email:
                print("Invalid email format. Please enter a valid email.")
                continue
            else:
                break

        address = input("Enter Your Address: ")

        # Create Customer Object
        cobj = Customer(P_username, password, name, dob_date, age, city, account_number, initial_balance, contact_number, email, address)
        cobj.createuser()
        print("Signup Successful!")
        
#SIGNIN / LOGIN
def SignIn():
    P_username = input("Enter Your account_number: ")
    
    # Check if account number exists in the database
    temp = db_query(f"SELECT username FROM customers WHERE account_number = '{P_username}';")
    
    if temp:
        while True:
            password = input("Enter Your Password: ")
            
            # Fetch the password for the provided account number
            db_password = db_query(f"SELECT password FROM customers WHERE account_number = '{P_username}';")
            
            # Ensure db_password contains data before checking the password
            if db_password and db_password[0][0] == password:
                print("Signed in successfully!")
                # Proceed to the main menu or function
                allcalls(P_username)
                break  # Exit the loop after successful sign-in
            else:
                print("Wrong password. Try again.")
                continue
    else:
        print("Account number not found. Please enter the correct account number.")
        SignIn()  # Retry if account number is not found
        

def show_user():
    account_number = input("Enter Your Account Number")
    cursor.execute(f"SELECT * FROM customers WHERE account_number = '{account_number}';")
    result = cursor.fetchone()
    
    if result:
        print("User Information:")
        print(f"Name: {result[2]}")
        print(f"Age: {result[3]}")
        print(f"DOB: {result[4]}")
        print(f"City: {result[5]}")
        print(f"Account Number: {result[6]}")
        print(f"Initial Balance: {result[7]}")
        print(f"Contact Number: {result[8]}")
        print(f"Email: {result[9]}")
        print(f"Address: {result[10]}")
        print(f"Account Status: {'Active' if result[11] else 'Inactive'}")
        print(f"Created At: {result[12]}")
    else:
        print("Account not found.")
