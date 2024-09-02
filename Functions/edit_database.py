import sqlite3
import os
from datetime import datetime
import pandas as pd
from uuid import uuid4 as randomID
from hashlib import sha256

from Functions.variables import Account
from Functions.client import *

def createDatabase() -> None:
    """
    Initializes the database by creating necessary tables if they do not exist.
    """
    if not os.path.exists("DB.db"):
        with open("DB.db", 'w'): pass
    else:
        return
    
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS accounts (
        USERNAME TEXT UNIQUE PRIMARY KEY,
        HASHED_PASSWORD INTEGER,
        SECURITY_QUESTION INTEGER,
        HASHED_SECURITY_ANSWER INTEGER,
        CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        BALANCE INT,
        TRANSACTIONS INT DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS miscellaneous (
        TYPE TEXT UNIQUE PRIMARY KEY,
        VALUE TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        TRANSACTION_ID TEXT UNIQUE PRIMARY KEY,
        USERNAME TEXT,
        ITEM TEXT,
        TYPE INTEGER,
        CATEGORY INTEGER,
        VALUE INTEGER,
        CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (USERNAME) REFERENCES accounts(USERNAME)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        MESSAGE_ID TEXT PRIMARY KEY,
        USERNAME TEXT,
        MESSAGE_TYPE INT,
        MESSAGE TEXT,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (USERNAME) REFERENCES accounts(USERNAME)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USERNAME TEXT,
        MESSAGE TEXT,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (USERNAME) REFERENCES accounts(USERNAME)
    )
    """)

    cursor.execute("INSERT INTO miscellaneous (TYPE, VALUE) VALUES (?, ?)", 
        ("last_user", "")
    )
    cursor.execute("INSERT INTO miscellaneous (TYPE, VALUE) VALUES (?, ?)", 
        ("times_opened", "")
    )
    cursor.execute("INSERT INTO miscellaneous (TYPE, VALUE) VALUES (?, ?)", 
        ("time_spent", "")
    )

    conn.commit()
    conn.close()

    addLog("Database created")

# Account functions
def addAccount(account:Account) -> str:
    """
    Add an account from the Account class to the account table
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO accounts (USERNAME, HASHED_PASSWORD, SECURITY_QUESTION, HASHED_SECURITY_ANSWER, BALANCE) VALUES (?, ?, ?, ?, ?)", 
            (account.username, 
            sha256(account.password.encode()).hexdigest(), 
            account.security_question, 
            sha256(account.security_answer.encode()).hexdigest(), 
            account.balance
            )
        )

        conn.commit()

        # Add account to online database
        # add_account(account)
        # if add_account(account):
        #     conn.close()
        #     return "Account added successfully"
        # else:
        #     conn.rollback()
        #     conn.close()
        #     return "Username already exists"

    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return "Username already exists"

def checkAccount(username:str, password:str) -> bool:
    """
    Check if the given username and password is correct
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    if row == None:
        # Check online database
        # if check_account(username, password):
        #     return True
        # else:
        return False
    else:
        return sha256(password.encode()).hexdigest() == row[1]

def checkSecurity(username:str, security_question:int, security_answer:str) -> bool:
    """
    Check if the given security question and answer is correct
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    if row == None:
        # Check online database
        # if check_security(username, security_question, security_answer):
        #     return True
        # else:
        return False
    else:
        return security_question == row[2] and sha256(security_answer.encode()).hexdigest() == row[3]
    
def updateBalance(account:Account, new_balance:int)-> str:
    """
    Updates the balance of a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE accounts SET BALANCE = ?, UPDATED_AT = ?, WHERE USERNAME = ?", 
            (new_balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), account.username)
        )

        conn.commit()
        conn.close()

        # Update online database
        # if update_balance(account.username, new_balance):
        #     return "Balance updated successfully"
        # else:
        #     return "Error updating balance"

    except Exception as e:
        return Exception(f"Error updating balance: {str(e)}")

def getAccount(username:str) -> Account:
    """
    Get the Account class from the given username
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        # Check online database
        # account = get_account(username)
        # if account is None:
        return None
        # else:
        #     return account
    else:
        return Account(row[0], row[1], row[2], row[3], row[4])

def editAccount(account:Account) -> str:
    """
    Updates the account information of a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE accounts SET HASHED_PASSWORD = ?, SECURITY_QUESTION = ?, HASHED_SECURITY_ANSWER = ?, UPDATED_AT = ?, WHERE USERNAME = ?", 
            (sha256(account.password.encode()).hexdigest(), 
            account.security_question, 
            sha256(account.security_answer.encode()).hexdigest(), 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            account.username)
        )

        conn.commit()
        conn.close()

        # Update online database
        # edit_account(account)
        # if edit_account(account):
        #     return "Account information updated successfully"
        # else:
        #     return "Error updating account information"
    except Exception as e:
        return f"Error updating account information: {str(e)}"

def deleteAccount(account:Account) -> str:
    """
    Deletes a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM accounts WHERE USERNAME = ?", 
            (account.username,)
        )

        conn.commit()
        conn.close()

        # Delete account from online database
        # delete_account(account.username)
        # if delete_account(account.username):
        #     return "Account deleted successfully"
        # else:
        #     return "Error deleting account"
    except Exception as e:
        return f"Error deleting account: {str(e)}"

def isUsernameAvailable(username:str) -> bool:
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM accounts WHERE USERNAME = ?", (username,))
        row = cursor.fetchone()
        #Check online database
        # if row is None and is_username_available(username):
        #     return True
        # else:
        #     return False
    finally:
        conn.close()

# Miscellaneous functions
def updateLastUser(username:str) -> None:
    """
    Updates the last user that logged in.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", (username, "last_user"))

    conn.commit()
    conn.close()

def getLastUser() -> Account:
    """
    Retrieves the last user that logged in.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT VALUE FROM miscellaneous WHERE TYPE = 'last_user'")

    row = cursor.fetchone()

    Account = getAccount(row[0])

    conn.close()

    return getAccount(row[0])

def updateTimesOpened() -> None:
    """
    Updates the number of times the program has been opened.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT VALUE FROM miscellaneous WHERE TYPE = ?", ("times_opened",))

    row = cursor.fetchone()

    if row == None:
        cursor.execute("INSERT INTO miscellaneous (TYPE, VALUE) VALUES (?, ?)", ("times_opened", 1))
    else:
        cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", (int(row[0]) + 1, "times_opened"))

    conn.commit()
    conn.close()

def getTimesOpened() -> int:
    """
    Retrieves the number of times the program has been opened.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT VALUE FROM miscellaneous WHERE TYPE = ?", ("times_opened",))

    row = cursor.fetchone()

    conn.close()

    return row[0]

def updateTimeSpent(start_time: datetime) -> None:
    """
    Updates the total time spent on the program.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    
    # Menghitung waktu yang dihabiskan
    time_spent = datetime.now() - start_time

    cursor.execute("SELECT VALUE FROM miscellaneous WHERE TYPE = ?", ("time_spent",))

    row = cursor.fetchone()

    if row is None:
        cursor.execute("INSERT INTO miscellaneous (TYPE, VALUE) VALUES (?, ?)", ("time_spent", time_spent).strftime("%H:%M:%S"))
    else:
        cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", ((row[0] + time_spent).strftime("%H:%M:%S"), "time_spent"))

    conn.commit()
    conn.close()

# # Contoh penggunaan (diletakkan di awal program)
# start_time = datetime.now()

def getTimeSpent() -> datetime:
    """
    Retrieves the total time spent on the program.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT VALUE FROM miscellaneous WHERE TYPE = ?", ("time_spent",))

    row = cursor.fetchone()

    conn.close()

    return row[0]

# Transaction functions
def addTransaction(account:Account, item: str, type:int, category: int, value: int, created_at:str = None, updated_at:str = None) -> str:
    """
    Inserts a transaction record into the transactions table.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    # harusnya ditambahin created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if updated_at == None:
        updated_at = created_at

    cursor.execute(
        "INSERT INTO transactions (TRANSACTION_ID, USERNAME, ITEM, TYPE, CATEGORY, VALUE, CREATED_AT, UPDATED_AT) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (id, account.username, item, type, category, value, created_at, updated_at)
    )

    conn.commit()

    cursor.execute("""
        UPDATE accounts
        SET TRANSACTIONS = TRANSACTIONS + 1
        WHERE USERNAME = ?
    """, (account.username,))

    conn.commit()

    # Add transaction to online database
    # add_transaction(id, account.username, item, type, category, value, created_at, updated_at)
    # if add_transaction(id, account.username, item, type, category, value, created_at, updated_at):
    #     conn.close()
    #     return "Transaction added successfully"
    # else:
    #     conn.rollback()
    #     conn.close()
    #     return "Error adding transaction"

def getTransaction(account:Account) -> pd.DataFrame:
    """
    Retrieves all transaction records as a Pandas DataFrame.
    """
    conn = sqlite3.connect("DB.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE USERNAME = ?", conn, params=(account.username,))
    conn.close()
    
    if df.empty:
        # Check online database
        # online_df = get_transaction(account.username)
        # if online_df is not None:
        #     return online_df
        # else:
        return pd.DataFrame()  # Return an empty DataFrame if no records found
    else:
        return df

def editTransaction(account: Account, transaction_id: str, item: str, type: int, category: int, value: int, updated_at: str = None) -> str:
    """
    Updates a transaction record.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try: 
        if updated_at is None:
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "UPDATE transactions SET ITEM = ?, TYPE = ?, CATEGORY = ?, VALUE = ?, UPDATED_AT = ? WHERE TRANSACTION_ID = ? AND USERNAME = ?", 
            (item, type, category, value, updated_at, transaction_id, account.username)
        )

        conn.commit()
        conn.close()

        # Update transaction in online database
        # edit_transaction(account.username, transaction_id, item, type, category, value, updated_at)
        # if edit_transaction(account.username, transaction_id, item, type, category, value, updated_at):
        #     return "Transaction information updated successfully"
        # else:
        #     return "Error updating transaction information"
    except Exception as e:
        return f"Error updating transaction information: {str(e)}"

def deleteTransaction(account:Account, transaction_id:str) -> str:
    """
    Deletes a transaction record.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "DELETE FROM transactions WHERE TRANSACTION_ID = ? AND USERNAME = ?", 
            (transaction_id, account.username)
        )

        conn.commit()
        conn.close()

        # Delete transaction from online database
        # delete_account(account.username)
        # if delete_account(account.username):
        #     return "Transaction deleted successfully"
        # else:
        #     return "Error deleting transaction"
    except Exception as e:
        return f"Error deleting transaction: {str(e)}"

# Chat functions
def addChats(username:str, message_type:int, message:str) -> str:
    """
    Inserts a chat message into the chats table.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    try:
        cursor.execute(
            "INSERT INTO chats (MESSAGE_ID, USERNAME, MESSAGE_TYPE, MESSAGE) VALUES (?, ?, ?, ?)", 
            (id, username, message_type, message)
        )

        conn.commit()
        conn.close()

        # Add chat to online database
        # add_chats(username, message_type, message, id)
        # if add_chats(username, message_type, message, id):
        #     return "Chat added successfully"
        # else:
        #     return "Error adding chat"
    except Exception as e:
        return f"Error adding chat: {str(e)}"

# Log functions
def addLog(message: str) -> None:
    """
    Inserts a log entry with a timestamp into the log table.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO log (MESSAGE, USERNAME) VALUES (?, ?)", 
        (message, "SYSTEM")
    )

    conn.commit()
    conn.close()

    # Add log to online database
    # add_log(message)