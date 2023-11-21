# import pandas as pd
import sqlite3
from prettytable import from_db_cursor

conn = sqlite3.connect('lab3.3.db')
curr = conn.cursor()

user_input = input("Enter the ACCOUNT_ID to delete: ")
curr.execute("SELECT cust_id, ACCOUNT_ID FROM ACCOUNT where CUST_ID = ? ", ( user_input, ) )
print(from_db_cursor(curr))
