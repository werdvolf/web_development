import sqlite3

from os import path, makedirs


CUR_PATH = path.dirname(path.abspath(__file__))

database_path = path.join(CUR_PATH, "../database")

orders_db_fn = "orders.db"


orders_db_fp = path.join(database_path, orders_db_fn)
order_db = sqlite3.connect(orders_db_fp)
order_db_cursor = order_db.cursor()



print(str(order_db_cursor.execute("SELECT * FROM orders")))
rows = order_db_cursor.fetchall()

for row in rows:
    print(row)