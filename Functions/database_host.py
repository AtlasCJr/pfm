import sqlite3
import os
from datetime import datetime
import pandas as pd
from uuid import uuid4 as randomID
from hashlib import sha256

from Functions.classes import Account

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
        BALANCE INT
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
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return "Username already exists"

    conn.close()
    return "Account added successfully"

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
            "UPDATE accounts SET BALANCE = ?, UPDATED_AT = ? WHERE USERNAME = ?", 
            (new_balance, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), account.username)
        )

        conn.commit()
        conn.close()

    except Exception as e:
        raise Exception(f"Error updating balance: {str(e)}")

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
        return None
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
            "UPDATE accounts SET HASHED_PASSWORD = ?, SECURITY_QUESTION = ?, HASHED_SECURITY_ANSWER = ?, UPDATED_AT = ? WHERE USERNAME = ?", 
            (sha256(account.password.encode()).hexdigest(), 
            account.security_question, 
            sha256(account.security_answer.encode()).hexdigest(), 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            account.username)
        )

        conn.commit()
        conn.close()

        return "Account information updated successfully"
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

        return "Account deleted successfully"
    except Exception as e:
        return f"Error deleting account: {str(e)}"

def isUsernameAvailable(username:str) -> bool:
    conn = sqlite3.connect("DB.db")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM accounts WHERE USERNAME = ?", (username,))
        row = cursor.fetchone()
        return row is not None
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

def getLastUser() -> str:
    """
    Retrieves the last user that logged in.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT VALUE FROM miscellaneous WHERE TYPE = ?", ("last_user",))

    row = cursor.fetchone()

    conn.close()

    return row[0]

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
def addTransaction(id: str, account:Account, item: str, type:int, category: int, value: int, created_at:str, updated_at:str = None) -> None:
    """
    Inserts a transaction record into the transactions table.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    if updated_at == None:
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO transactions (TRANSACTION_ID, USERNAME, ITEM, TYPE, CATEGORY, VALUE, CREATED_AT, UPDATED_AT) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (id, account.username, item, type, category, value, created_at, updated_at)
    )

    conn.commit()
    conn.close()

def getTransaction(account:Account) -> pd.DataFrame:
    """
    Retrieves all transaction records as a Pandas DataFrame.
    """
    conn = sqlite3.connect("DB.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE USERNAME = ?", conn, params=(account.username,))
    conn.close()
    
    return df

def editTransaction(account: Account, transaction_id: str, item: str, type: int, category: int, value: int, created_at: str, updated_at: str = None) -> None:
    """
    Updates a transaction record.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    if updated_at is None:
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "UPDATE transactions SET ITEM = ?, TYPE = ?, CATEGORY = ?, VALUE = ?, CREATED AT = ?, UPDATED_AT = ? WHERE TRANSACTION_ID = ? AND USERNAME = ?", 
        (item, type, category, value, created_at, updated_at, transaction_id, account.username)
    )

    conn.commit()
    conn.close()

def deleteTransaction(account:Account, transaction_id:str) -> None:
    """
    Deletes a transaction record.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE TRANSACTION_ID = ? AND USERNAME = ?", 
        (transaction_id, account.username)
    )

    conn.commit()
    conn.close()

# Chat functions
def addChats(username:str, message_type:int, message:str, id:str = None) -> None:
    """
    Inserts a chat message into the chats table.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    if id is None:
        id = str(randomID())

    cursor.execute(
        "INSERT INTO chats (MESSAGE_ID, USERNAME, MESSAGE_TYPE, MESSAGE) VALUES (?, ?, ?, ?)", 
        (id, username, message_type, message)
    )

    conn.commit()
    conn.close()

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