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


def get_password(email):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    cursor.execute('SELECT password FROM user WHERE email = ?;', (email,))
    password = cursor.fetchall()

    return password