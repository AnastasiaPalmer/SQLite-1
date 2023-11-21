# import pandas as pd
import sqlite3
from prettytable import from_db_cursor

conn = sqlite3.connect('lab3.3.db')
# conn = sqlite3.connect('/users/nasti/Downloads/Лаб 3.4.db')
curr = conn.cursor()

"""

Кожне питання повинні вирішуватись лише 1 запитом до БД.
1. Огляд даних:

 a. Створіть метод, який буде виводити визначену таблицю з БД у вигляді таблиці у консоль
    (використайте columnar або prettytable). Для прикладу, візьміть таблицю Customer.

"""

curr.execute('''SELECT * FROM Customer''')
print(from_db_cursor(curr))

"""

2. Створення звітів та запитів на звіти:

 a. Виведіть всі дані співробітників по кожному з департаментів 
    (читайте: згрупованих по кожному з департаментів)
 b. Виведіть всі дані, що стосуються CUST_ID 10 з таблиць CUSTOMER, ACCOUNT, OFFICER.
 c. Виведіть всі AVAIL_BALANCE та відповідні CITY, які більші за 3000.
 d. Виведіть всі відкриті рахунки з 2004 року, що стосуються 
    home mortgage, savings account, small business loan
 e. Виведіть всіх клієнтів (з Customers) які користуються Insurance Offerings

"""
curr.execute('''SELECT * FROM Employee ORDER BY TITLE''')
print(from_db_cursor(curr))

curr.execute('''select * from (
                SELECT *
                FROM CUSTOMER
                JOIN ACCOUNT on CUSTOMER.CUST_ID = ACCOUNT.ACCOUNT_ID
                JOIN OFFICER on CUSTOMER.CUST_ID = OFFICER.CUST_ID
                WHERE CUSTOMER.CUST_ID = '10'
                )
''')
print(from_db_cursor(curr))

curr.execute('''SELECT ACCOUNT_ID, CITY, AVAIL_BALANCE FROM CUSTOMER
                JOIN ACCOUNT on ACCOUNT.account_id = CUSTOMER.cust_id
                WHERE AVAIL_BALANCE >= 3000
                ORDER BY CITY
''')
print(from_db_cursor(curr))

curr.execute('''select * from(
                SELECT date(OPEN_DATE) as date_only, *
                FROM ACCOUNT
                JOIN PRODUCT on product.product_cd = account.product_cd
                WHERE 1=1
                AND date(OPEN_DATE) > '2004-01-01'
                AND product.name in ('home mortgage', 'savings account', 'small business loan'))
''')
print(from_db_cursor(curr))

curr.execute('''
                SELECT c.cust_id, i.first_name, a.avail_balance, a.open_date, a.product_cd
                , p.product_type_cd
                , t.name as tname
                FROM CUSTOMER c
                join individual i on i.cust_id = c.cust_id
                JOIN ACCOUNT  a on a.cust_id = c.cust_id
                JOIN PRODUCT  p on p.product_cd = a.product_cd
                JOIN PRODUCT_TYPE t on t.product_type_cd = p.product_type_cd
                WHERE t.NAME like 'Insurance Offerings'
                --where c.cust_id in(1,2)

''')

print(from_db_cursor(curr))

"""

3. Створення функцій для редагування даних:

 a. Створіть функцію, яка буде видаляти рядки по всім таблицям бази, які відповідають ACCOUNT_ID,
    яке вводить користувач
 b. Створіть функцію, яка допоможе користувачу додавати дані до таблиці CUSTOMER
 c. Створіть функцію, яка буде дозволяти користувачу редагувати поле AVAIL_BALANCE (стовпець, за 
    яким можна буде обирати конкретне значення виберіть самі)

"""
from string import Template

user_input = input("Enter the ACCOUNT_ID to delete: ")

shablon = 'Delete * FROM ACCOUNT where CUST_ID = $id'
query = Template(shablon).substitute(id=user_input)
curr.execute(query)

print(from_db_cursor(curr))

# user_input = input("Enter the ACCOUNT_ID to delete: ")
# curr.execute("""
#     SELECT cust_id FROM ACCOUNT where CUST_ID = %s
#     """, [int(user_input)] )
# print(from_db_cursor(curr))

def add_customer(curr):
    c_id = input("Enter ID: ")
    addres = input("Enter ADDRESS: ")
    city = input("Enter CITY: ")
    cd = input("Enter CUST TYPE CD: ")
    fed_id = input("Enter FED ID: ")
    pc = input("Enter POSTAL CODE: ")
    state = input("Enter STATE: ")

    query = f"INSERT INTO CUSTOMER (CUST_ID, ADDRESS, CITY, CUST_TYPE_CD, FED_ID, POSTAL_CODE, STATE) " \
            f"VALUES ('{c_id}', '{addres}', '{city}', '{cd}', '{fed_id}', '{pc}', '{state}')"

    curr.execute(query)
    curr.execute('COMMIT')

    print("Customer added successfully!", query)


add_customer(curr)

curr.execute('''SELECT * FROM CUSTOMER''')
print(from_db_cursor(curr))

# Customer added successfully!
# INSERT INTO CUSTOMER (CUST_ID, ADDRESS, CITY, CUST_TYPE_CD, FED_ID, POSTAL_CODE, STATE)
# VALUES ('20', '222 st', 'misto', 'B', '07-4444444', '2222', 'BU')

"""Створіть функцію, яка буде дозволяти користувачу редагувати поле AVAIL_BALANCE 
   (стовпець, за яким можна буде обирати конкретне значення виберіть самі)       """


def change_balance(curr):
    i_cust = input("Enter cust id [0]      : ")
    i_acc  = input("Enter acc  id [0]      : ")
    a_bal = input("Enter the AVAIL_BALANCE: ")

    condition = f"""
         where 1=1
           and ( {i_cust} = 0  or  CUST_ID    = {i_cust} )
           and ( {i_acc}  = 0  or  ACCOUNT_ID = {i_acc} )"""

    query1 = f"select cust_id, account_id, avail_balance, open_date, status from ACCOUNT {condition}"
    curr.execute(query1)
    print(from_db_cursor(curr))

    yes = input('Are you sure you want to delete records previous ? (Y) : ')
    query2 = f"""
        update account 
           set avail_balance={a_bal} 
         {condition}
    """
    if yes == 'Y':
        curr.execute(query2)
        #curr.execute('COMMIT')
    else:
        print('Canseled:', query2)


change_balance(curr)

curr.execute('''SELECT * FROM ACCOUNT''')
print(from_db_cursor(curr))
