import sqlite3
import os
from datetime import datetime
import pandas as pd
from uuid import uuid4 as randomID
from hashlib import sha256

from Functions._Variables import Account

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
        USER_ID TEXT PRIMARY KEY,
        USERNAME TEXT UNIQUE,
        HASHED_PASSWORD INTEGER,
        CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        BALANCE INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        TRANSACTION_ID TEXT PRIMARY KEY,
        USER_ID TEXT,
        ITEM TEXT,
        TYPE INTEGER,
        CATEGORY INTEGER,
        VALUE INTEGER,
        CREATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        UPDATED_AT DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (USER_ID) REFERENCES accounts(USER_ID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        MESSAGE_ID TEXT PRIMARY KEY,
        USER_ID TEXT,
        MESSAGE_TYPE INT,
        MESSAGE TEXT,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (USER_ID) REFERENCES accounts(USER_ID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MESSAGE TEXT NOT NULL,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    addLog("Database created")

    conn.commit()
    conn.close()

def addLog(message: str) -> None:
    """
    Inserts a log entry with a timestamp into the log table.
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO log (MESSAGE) VALUES (?)", 
        (message, )
    )

    conn.commit()
    conn.close()

def addTransaction(account:Account, item: str, type:int, category: int, value: int, created_at:str = None) -> None:
    """
    Inserts a transaction record into the transactions table.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    if created_at == None:
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO transactions (TRANSACTION_ID, USER_ID, ITEM, TYPE, CATEGORY, VALUE, CREATED_AT, UPDATED_AT) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
        (id, account.user_id, item, type, category, value, created_at, created_at)
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
            "INSERT INTO accounts (USER_ID, USERNAME, HASHED_PASSWORD, BALANCE) VALUES (?, ?, ?, ?)", 
            (account.user_id, account.username, sha256(account.password.encode()).hexdigest(), account.balance)
        )
    except:
        return

    conn.commit()
    conn.close()

def updateBalance(account:Account, new_balance:int) -> None:
    """
    Updates the balance of a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE accounts SET BALANCE = ? WHERE USER_ID = ?", 
        (new_balance, account.user_id)
    )

    conn.commit()
    conn.close()

def getTransactionData(account:Account) -> pd.DataFrame:
    """
    Retrieves all transaction records as a Pandas DataFrame.
    """
    conn = sqlite3.connect("DB.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE USER_ID = ?", conn, params=(account.user_id,))
    conn.close()
    
    return df

def getAccount(username:str):
    """
    Get the Account class from the given username
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    account = Account(row[1], row[2], row[3], row[4], row[5], row[0])
    
    return account