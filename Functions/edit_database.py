import sqlite3
import os
from datetime import datetime
import pandas as pd
from uuid import uuid4 as randomID
from hashlib import sha256

from Functions.variables import Account

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

def addTransaction(account:Account, item: str, type:int, category: int, value: int, created_at:str = None, updated_at:str = None) -> None:
    """
    Inserts a transaction record into the transactions table.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    if updated_at == None:
        updated_at = created_at

    cursor.execute(
        "INSERT INTO transactions (TRANSACTION_ID, USERNAME, ITEM, TYPE, CATEGORY, VALUE, CREATED_AT, UPDATED_AT) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (id, account.username, item, type, category, value, created_at, updated_at)
    )

    conn.commit()
    conn.close()

def addAccount(account:Account) -> None:
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
             account.security_answer, 
             account.balance
            )
        )

        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return "Username already exists"

    conn.close()

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

def checkSecurityAnswer(username:str, security_answer:str) -> bool:
    """
    Check if the given security answer is correct
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    if row == None:
        return False
    else:
        return sha256(security_answer.encode()).hexdigest() == row[3]
    
def updateBalance(account:Account, new_balance:int) -> None:
    """
    Updates the balance of a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE accounts SET BALANCE = ? WHERE USERNAME = ?", 
        (new_balance, account.username)
    )

    conn.commit()
    conn.close()

def addMiscellaneous(account:Account) -> None:
    """
    Adds a miscellaneous field to a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    cursor.execute(
        "INSERT INTO miscellaneous (MISCELLANEOUS_ID, USERNAME) VALUES (?, ?)", 
        (id, account.username)
    )

    conn.commit()
    conn.close()

def deleteMiscellaneous(account:Account) -> None:
    """
    Deletes a miscellaneous field from a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM miscellaneous WHERE USERNAME = ?", 
        (account.username,)
    )

    conn.commit()
    conn.close()

def getTransactionData(account:Account) -> pd.DataFrame:
    """
    Retrieves all transaction records as a Pandas DataFrame.
    """
    conn = sqlite3.connect("DB.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE USERNAME = ?", conn, params=(account.username,))
    conn.close()
    
    return df

def getAccount(username:str) -> Account:
    """
    Get the Account class from the given username
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    account = Account(row[0], row[1], row[2], row[3], row[4])
    
    return account

def addChats(username:str, message_type:int, message:str) -> None:
    """
    Inserts a chat message into the chats table.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    cursor.execute(
        "INSERT INTO chats (MESSAGE_ID, USERNAME, MESSAGE_TYPE, MESSAGE) VALUES (?, ?, ?, ?)", 
        (id, username, message_type, message)
    )

    conn.commit()
    conn.close()

def isUsernameAvailable(username:str) -> bool:
    conn = sqlite3.connect("DB.db")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM accounts WHERE USERNAME = ?", (username,))
        row = cursor.fetchone()
        return row is not None
    finally:
        conn.close()