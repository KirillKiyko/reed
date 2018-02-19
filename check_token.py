import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def check_token(email):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    data = (email,)

    cursor.execute('SELECT token FROM user WHERE email = ?', data)
    status = cursor.fetchall()

    return status