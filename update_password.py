import sqlite3
import re

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def update_password(password, email):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    cursor.execute('UPDATE user SET password = ? WHERE email = ?', (password, email))
    conn.commit()