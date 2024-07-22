import sqlite3
import os
from datetime import datetime
import pandas as pd

def createDatabase() -> None:
    if not os.path.exists("DB.sql"):
        with open("DB.sql", 'w'): pass
    else:
        return
    
    conn = sqlite3.connect("DB.sql")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ITEM TEXT,
        TYPE INTEGER,
        VALUE INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS log (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        DATE TEXT,
        CONTENT TEXT
    )
    """)

    addLog("Database created")

    conn.commit()
    conn.close()

def addLog(content:str) -> None:
    conn = sqlite3.connect("DB.sql")
    cursor = conn.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO log (DATE, CONTENT) VALUES (?, ?)
    """, (now, content))

    conn.commit()
    conn.close()

def addTransaction(item:str, type:int, value:int) -> None:
    conn = sqlite3.connect("DB.sql")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO transactions (ITEM, TYPE, VALUE) VALUES (?, ?, ?)
    """, (item, type, value))

    conn.commit()
    conn.close()

def getTransactionData() -> pd.DataFrame:
    df = pd.read_sql_query("SELECT * FROM transactions")
    return df

if __name__ == "__main__":
    os.system("cls" if os.name =="nt" else "clear")
    createDatabase()

    addTransaction("Beli Ayam", 1, 10000)