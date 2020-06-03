import sqlite3

from os import path, makedirs


class DB_Exception(Exception):
    pass


# The path to directory this code is ran in.
CUR_PATH = path.dirname(path.abspath(__file__))

database_path = path.join(CUR_PATH, "../database")

# Users database filename.
users_db_fn = "users.db"
orders_db_fn = "orders.db"

# Users database filepath.
users_db_fp = path.join(database_path, users_db_fn)
orders_db_fp = path.join(database_path, orders_db_fn)


def init_user_database():
    # Create file, and dirs, if those do not exist.
    makedirs(database_path, exist_ok=True)
    with open(users_db_fp, "w+"):
        pass

    user_db = sqlite3.connect(users_db_fp)
    user_db_cursor = user_db.cursor()
    user_db_cursor.execute(
        """
        CREATE TABLE users
        (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        permissions INTEGER)
        """
    )
def init_order_database():
    makedirs(database_path, exist_ok=True)
    with open(orders_db_fp, "w+"):
        pass
    order_db = sqlite3.connect(orders_db_fp)
    order_db_cursor = order_db.cursor()
    order_db_cursor.execute(
        """
        CREATE TABLE orders
        (order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        min_budget FLOAT ,
        max_budget FLOAT ,
        media_ad_type int ,
        tv_ad_type int ,
        outdoor_ad_type int ,
        product_placement_ad_type int ,
        radio_ad_type int ,
        description_ad_type TEXT)
        """

    )


def init_databases():
    init_user_database()
    init_order_database()


def setup():
    init_databases()


if __name__ == "__main__":
    setup()
else:
    if not path.exists(users_db_fp):
        init_user_database()
    if not path.exists(orders_db_fp):
        init_order_database()

user_db = sqlite3.connect(users_db_fp)
order_db = sqlite3.connect(orders_db_fp)
# A cursor for work with user database.
user_db_cursor = user_db.cursor()
order_db_cursor = order_db.cursor()
