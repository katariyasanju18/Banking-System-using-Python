from Database import *
from datetime import datetime
class Customer:
    def __init__(self, username, password, name, dob, age, city, account_number, initial_balance, contact_number, email, address):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__dob = dob  # Added dob to the constructor
        self.__age = age
        self.__city = city
        self.__account_number = account_number
        self.__initial_balance = initial_balance
        self.__contact_number = contact_number
        self.__email = email
        self.__address = address
    
    def createuser(self):
        query = f"""
            INSERT INTO customers 
            (username, password, name, dob, age, city, account_number, initial_balance, contact_number, email_id, address, user_status)
            VALUES ('{self.__username}', '{self.__password}', '{self.__name}', '{self.__dob.strftime('%Y-%m-%d')}', '{self.__age}', '{self.__city}', '{self.__account_number}', '{self.__initial_balance}', '{self.__contact_number}', '{self.__email}', '{self.__address}', 1);
        """
        db_query(query)
        mydb.commit()
        