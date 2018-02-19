import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def get_title(link):
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    data = (link,)

    cursor.execute('SELECT title FROM summarization WHERE url = ?', data)
    status = cursor.fetchall()

    return status