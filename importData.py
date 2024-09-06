import pandas as pd
from tqdm import tqdm 
from Functions.database import *
from Functions.classes import Account

createDatabase()

myAccount = Account("user1", "user1_template", 1, "depok", "2023-05-10 13:35:47", "2023-05-10 13:35:47", 0)
addAccount(myAccount)

df = pd.read_csv("Data Creation/DATA1.csv")
for index, row in tqdm(df.iterrows()):
    addTransaction(myAccount, row['ITEM'], row['TYPE'], row['CATEGORY'], row['VALUE'], row['CREATED_AT'])

myAccount = Account("user2", "user2_template", 1, "jakarta", "2022-05-11 13:47:35", "2023-05-10 13:37:35", 0)
addAccount(myAccount)

df = pd.read_csv("Data Creation/DATA2.csv")
for index, row in tqdm(df.iterrows()):
    addTransaction(myAccount, row['ITEM'], row['TYPE'], row['CATEGORY'], row['VALUE'], row['CREATED_AT'])