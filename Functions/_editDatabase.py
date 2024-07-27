import sqlite3
import os
from datetime import datetime
import pandas as pd
from uuid import uuid4 as randomID

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
        USERNAME TEXT,
        HASHED_PASSWORD INTEGER,
        CREATED_AT TEXT,
        UPDATED_AT TEXT,
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
        CREATED_AT TEXT,
        UPDATED_AT TEXT,
        FOREIGN KEY (USER_ID) REFERENCES accounts(USER_ID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        MESSAGE_ID TEXT PRIMARY KEY,
        USER_ID TEXT,
        MESSAGE_TYPE INT,
        MESSAGE TEXT,
        TIMESTAMP TEXT,
        FOREIGN KEY (USER_ID) REFERENCES accounts(USER_ID)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MESSAGE TEXT,
        TIMESTAMP TEXT
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

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO log (TIMESTAMP, MESSAGE) VALUES (?, ?)
    """, (now, message))

    conn.commit()
    conn.close()

def addTransaction(item: str, type:int, category: int, value: int, created_at: str = None, updated_at: str = None) -> None:
    """
    Inserts a transaction record into the transactions table.
    """
    if created_at is None:
        created_at = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    if updated_at is None:
        updated_at = created_at
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    id = str(randomID())

    cursor.execute("""
    INSERT INTO transactions (TRANSACTION_ID, USER_ID, ITEM, TYPE, CATEGORY, VALUE, CREATED_AT, UPDATED_AT) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (id, "asdasd", item, type, category, value, created_at, updated_at))

    conn.commit()
    conn.close()

def getTransactionData() -> pd.DataFrame:
    """
    Retrieves all transaction records as a Pandas DataFrame.
    """
    conn = sqlite3.connect("DB.db")
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    createDatabase()

    addTransaction("Ayam Goreng", 1, 1, 20000)

    print(getTransactionData())
