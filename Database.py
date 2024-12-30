import mysql.connector as sql

# Connect to the database
mydb = sql.connect(
    host="Host_name",
    user="User_name",
    password="Your_password",
    database="Your Database Name"
)

cursor = mydb.cursor()

# Create the customers table if it doesn't exist
def createcustomertable():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        username VARCHAR(20) NOT NULL,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(50) NOT NULL,
        age INT,
        dob DATE NOT NULL,
        city VARCHAR(50) NOT NULL,
        account_number CHAR(10) UNIQUE NOT NULL,
        initial_balance INTEGER CHECK (initial_balance >= 2000) NOT NULL, 
        contact_number CHAR(10) UNIQUE NOT NULL,
        email_id VARCHAR(100) UNIQUE NOT NULL,
        address VARCHAR(255) NOT NULL,
        user_status BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
        PRIMARY KEY (account_number)
    );
    ''')

# Create the login table if it doesn't exist
def logintable():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS login (
        account_number CHAR(10) UNIQUE NOT NULL,                    
        password VARCHAR(255) NOT NULL,            
        FOREIGN KEY (account_number) REFERENCES customers(account_number) 
    );
    ''')

# Create the transaction table if it doesn't exist
def transactiontable():
    cursor.execute('''
CREATE TABLE IF NOT EXISTS transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,  
    account_number CHAR(10) NOT NULL,                             -- account_number is not unique
    transaction_type ENUM('credit', 'debit', 'transfer') NOT NULL, 
    amount DECIMAL(10, 2) NOT NULL,                 
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
    to_account_number CHAR(10),   
    FOREIGN KEY (account_number) REFERENCES customers(account_number) 
);
    ''')

# Commit the changes
mydb.commit()

# Function to run queries and return results
def db_query(query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result

# Main execution
if __name__ == "__main__":
    createcustomertable()
    logintable()
    transactiontable()