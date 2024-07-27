"""


JANGAN DI RUN LAGI
INI CUMA BUAT MASUKIN DATA DARI DATA CREATION KE SQL



"""


import pandas as pd
from tqdm import tqdm 
from Functions._editDatabase import *
from Functions._Variables import Account




createDatabase()

myAccount = Account("atlas", "skibidi", "2023-05-10 13:35:47", "2023-05-10 13:35:47", 10_000_000)

addAccount(myAccount)



df = pd.read_csv("Data Creation/DATA.csv")

for index, row in tqdm(df.iterrows()):
    # if index < 5000:
    #     addTransaction(myAccount, row['ITEM'], row['TYPE'], row['CATEGORY'], row['VALUE'], row['CREATED_AT'])
    # else:
    #     break

    addTransaction(myAccount, row['ITEM'], row['TYPE'], row['CATEGORY'], row['VALUE'], row['CREATED_AT'])