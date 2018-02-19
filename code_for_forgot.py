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


def code_for_forgot(code, email):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    data = (code, email)

    try:
        cursor.execute('UPDATE user SET code = ? WHERE email = ?', data)
        conn.commit()
        code = cursor.fetchall()

        return code
    except Exception:
        return 'Incorrect email'