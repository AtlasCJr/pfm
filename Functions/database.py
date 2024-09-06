import sqlite3
import os
from datetime import datetime
import pandas as pd
from uuid import uuid4 as randomID
from hashlib import sha256

from Functions.classes import Account
from Functions import database_client as dc

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
    CREATE TABLE IF NOT EXISTS log (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        MESSAGE TEXT,
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP
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
            sha256(account.security_answer.encode()).hexdigest(), 
            account.balance
            )
        )

        conn.commit()

        addLog(f"Account {account.username} added successfully")

        # Add account to online database
        # dc._addAccount(account)
        # if dc._addAccount(account):
        #     conn.close()
        #     addLog("Account added in online successfully")
        # else:
        #     conn.rollback()
        #     conn.close()
        #     addLog("Failed added account in online")

    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        addLog(f"Failed added account {account.username}: Username already exists")

def checkAccount(username:str, password:str) -> bool:
    """
    Check if the given username and password is correct
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    # if row == None:
        # Check online database
        # if dc._checkAccount(username, password):
        #     return True
        # else:
        #     return False
    # else:
    return sha256(password.encode()).hexdigest() == row[1]

def checkSecurity(username:str, security_answer:str) -> bool:
    """
    Check if the given security question and answer is correct
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    # if row == None:
        # Check online database
        # if dc._checkSecurity(username, security_question, security_answer):
        #     return True
        # else:
        #     return False
    # else:
    return sha256(security_answer.encode()).hexdigest() == row[3]
    
def updateBalance(account:Account)-> None:
    """
    Updates the balance of a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        df = getTransaction(account)
        new_balance = 0
        for _, row in df.iterrows():
            if row['CATEGORY'] == 0:
                new_balance -= row['VALUE']
            else:
                new_balance += row['VALUE']

        cursor.execute(
            "UPDATE accounts SET BALANCE = ? WHERE USERNAME = ?", 
            (new_balance, account.username)
        )

        conn.commit()
        conn.close()

        addLog(f"Balance {account.username} updated successfully")

        # Update online database
        # if dc._updateBalance(account.username, new_balance):
        #     addLog("Balance updated in online successfully")
        # else:
        #     addLog("Error updating balance in online")

    except Exception as e:
        addLog(f"Error updating balance {account.username}: {str(e)}")

def getAccount(username:str) -> Account:
    """
    Get the Account class from the given username
    """
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM accounts WHERE USERNAME = ?", (username,))

    row = cursor.fetchone()

    conn.close()

    updateLastUser(row[0])

    # if row is None:
        # # Check online database
        # account = dc._getAccount(username)
        # if account is None:
        #     return None
        # else:
        #     return account
    # else:
    return Account(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])

def editAccount(account:Account) -> None:
    """
    Updates the account information of a user account.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE accounts SET HASHED_PASSWORD = ?, UPDATED_AT = ? WHERE USERNAME = ?", 
            (sha256(account.password.encode()).hexdigest(), 
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            account.username)
        )

        conn.commit()
        conn.close()

        addLog(f"Account {account.username} updated successfully")

        #Update online database
        # dc._editAccount(account)
        # if dc._editAccount(account):
        #     addLog("Account information updated in online successfully")
        # else:
        #     addLog("Error updating account information in online")
    except Exception as e:
        addLog(f"Error updating account information {account.username}: {str(e)}")

def deleteAccount(account:Account) -> None:
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

        addLog(f"Account {account.username} deleted successfully")

        # Delete account from online database
        # dc._deleteAccount(account.username)
        # if dc._deleteAccount(account.username):
        #     addLog("Account deleted in online successfully")
        # else:
        #     addLog("Error deleting account in online")
    except Exception as e:
        addLog(f"Error deleting account {account.username}: {str(e)}")

def isUsernameAvailable(username:str) -> bool:
    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT 1 FROM accounts WHERE USERNAME = ?", (username,))
        row = cursor.fetchone()

        if row is None and not dc._isUsernameAvailable(username):
            return False
        else:
            return True
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

    if row[0] == '':
        cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", (str(1), "times_opened"))
    else:
        cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", (str(int(row[0]) + 1), "times_opened"))

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

    # print(time_spent)

    if row[0] == '':
        cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", (str(time_spent).split('.')[0], "time_spent"))
    else:
        initial_time = datetime.strptime(row[0], "%H:%M:%S")
        new_time = (initial_time + time_spent).time().strftime("%H:%M:%S")
        cursor.execute("UPDATE miscellaneous SET VALUE = ? WHERE TYPE = ?", (new_time, "time_spent"))

    conn.commit()
    conn.close()

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
def addTransaction(account:Account, item: str, type:int, category: int, value: int, created_at:str) -> None:
    """
    Inserts a transaction record into the transactions table.
    """

    try:
        conn = sqlite3.connect("DB.db")
        cursor = conn.cursor()
        id = str(randomID())

        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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

        addLog(f"Transaction {id} added successfully")

        # # Add transaction to online database
        # _addTransaction(id, account.username, item, type, category, value, created_at, updated_at)
        # if _addTransaction(id, account.username, item, type, category, value, created_at, updated_at):
        #     conn.close()
        #     addLog("Transaction added in online successfully")
        # else:
        #     conn.rollback()
        #     conn.close()
        #     addLog("Error adding transaction in online")
        conn.close()
    
    except Exception as e:
        addLog(f"Error adding transaction: {str(e)}")

def getTransaction(account:Account) -> pd.DataFrame:
    """
    Retrieves all transaction records as a Pandas DataFrame.
    """
    conn = sqlite3.connect("DB.db")
    df = pd.read_sql_query("SELECT * FROM transactions WHERE USERNAME = ?", conn, params=(account.username,))
    conn.close()
    
    if df.empty:
        # Check online database
        # online_df = _getTransaction(account.username)
        # if online_df is not None:
        #     return online_df
        # else:
        return pd.DataFrame()  # Return an empty DataFrame if no records found
    else:
        return df

def editTransaction(account: Account, transaction_id: str, item: str, type: int, category: int, value: int, created_at: str) -> None:
    """
    Updates a transaction record.
    """

    conn = sqlite3.connect("DB.db")
    cursor = conn.cursor()

    try: 
        updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "UPDATE transactions SET ITEM = ?, TYPE = ?, CATEGORY = ?, VALUE = ?, CREATED_AT = ?, UPDATED_AT = ? WHERE TRANSACTION_ID = ? AND USERNAME = ?", 
            (item, type, category, value, created_at, updated_at, transaction_id, account.username)
        )

        conn.commit()
        conn.close()

        addLog(f"Transaction {transaction_id} edited successfully")

        # Update transaction in online database
        # _editTransaction(account.username, transaction_id, item, type, category, value, created_at, updated_at)
        # if _editTransaction(account.username, transaction_id, item, type, category, value, created_at, updated_at):
        #     addLog("Transaction information updated in online successfully")
        # else:
        #     addLog("Error updating transaction information in online")
    except Exception as e:
        addLog(f"Error edited transaction {transaction_id} information: {str(e)}")

def deleteTransaction(account:Account, transaction_id:str) -> None:
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

        cursor.execute("""
            UPDATE accounts
            SET TRANSACTIONS = TRANSACTIONS - 1
            WHERE USERNAME = ?
        """, (account.username,))

        conn.commit()
        conn.close()

        addLog(f"Transaction {transaction_id} deleted successfully")

        # # Delete transaction from online database
        # dc._deleteTransaction(account.username, transaction_id)
        # if dc._deleteTransaction(account.username, transaction_id):
        #     addLog("Transaction deleted in online successfully")
        # else:
        #     addLog("Error deleting transaction in online")
    except Exception as e:
        addLog(f"Error deleting transaction {transaction_id}: {str(e)}")

# Log functions
def addLog(message: str) -> None:
    """
    Inserts a log entry with a timestamp into the log table.
    """
    try:
        conn = sqlite3.connect("DB.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO log (MESSAGE) VALUES (?)", 
            (message,)
        )

        conn.commit()
    except Exception as e:
        print(f"Error inserting log: {str(e)}")
    finally:
        conn.close()

    # Add log to online database
    # dc._addLog(message)