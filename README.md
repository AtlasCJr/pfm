# Personal Finance Manager

A personal finance manager (PFM) is a tool or software designed to help individuals manage their financial activities effectively. It provides features for tracking income, expenses, budgeting, saving, investing, and managing debts. The goal of a PFM is to help users gain better control over their finances, make informed decisions, and achieve their financial goals.

#### Created By
- Jonathan Edward Charles De Fretes     
- Davin Nazhif Wilviadli     
- Muhammad Farhan Hanafi

#### Features
- Multiple accounts
- Embedded database system (potentially online)
- Internal model prediction
- Internal chatbot

#### Database
The database consist is created in SQLite. There are 4 + 1 tables in the database:
+ Accounts
    * User Id  <-- Primary Key
    * Username
    * Hashed Password
    * Created At
    * Updated At
    * Security Question
    * Security Answer

+ Chats
    * Message Id <-- Primary Key
    * User Id <-- Foreign Key
    * Message Type
    * Message
    * Timestap

+ Log
    * ID <-- Primary Key
    * Message
    * Timestamp

+ Transaction
    * Transaction Id <-- Primary Key
    * User Id <-- Foreign 
    * Item
    * Type
    * Category
    * Value
    * Created At
    * Updated At

+ Miscellaneous
    * Type <-- Primary Key
    * Value

and one more table _sqlite_sequences_ which hold account the incrementation for 'Log' and some data in 'Miscellaneous'.

#### Updates
28/08/2024
+ Added the final home page

#### Temporary Copy-Paste
pyuic5 -x UI/Master.ui -o UI/Master.py 