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


def check_forgot_user(email):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    cursor.execute('SELECT status FROM user WHERE email = ?;', (email,))
    status = cursor.fetchall()

    return status