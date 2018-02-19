import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def change_mobile_status(mobile_status, email):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    cursor.execute('UPDATE user SET mobile_status = ? WHERE email = ?;', (mobile_status, email))
    conn.commit()