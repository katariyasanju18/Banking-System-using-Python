from Register import *

# USER REGISTRATION SYSTEM
def display_menu():
    print("\n1. SIGNUP")
    print("2. SHOW USER")
    print("3. SIGNIN")
    print("4. EXIT")

while True:
    try:
        display_menu()  # Display the menu
        register = int(input("Please choose an option (1-4): "))
        
        if register == 1:
            Signup()
        elif register == 2:
            show_user()
        elif register == 3:
            SignIn()
        elif register == 4:
            print("THANK YOU FOR VISITING THE BANK!")
            break
        else:
            print("Please enter a valid number from the options (1-4).")
    
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 4.")