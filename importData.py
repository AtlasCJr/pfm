"""

JANGAN DI RUN LAGI
INI CUMA BUAT MASUKIN DATA DARI DATA CREATION KE SQL

"""


import pandas as pd
from tqdm import tqdm 
from Functions.edit_database import *
from Functions.variables import Account

createDatabase()

myAccount = Account("atlas", "skibidi", 1, "Depok", "2023-05-10 13:35:47", "2023-05-10 13:35:47", 10_000_000)
addAccount(myAccount)

df = pd.read_csv("Data Creation/DATA.csv")
for index, row in tqdm(df.iterrows()):
    addTransaction(myAccount, row['ITEM'], row['TYPE'], row['CATEGORY'], row['VALUE'], row['CREATED_AT'])