import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def find_user(conn):
    status = ('publish',)
    sql = '''SELECT count(id) FROM summarization WHERE status = ?;'''

    cur = conn.cursor()
    cur.execute(sql, status)
    return cur.fetchall()


def get_rownum():
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        try:
            number = find_user(conn)
            return number
        except Exception:
            return 'No summary'


if __name__ == '__main__':
    get_rownum()