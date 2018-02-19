import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def find_mysummary(conn, id):
    sql = '''SELECT count(id) FROM summarization WHERE user_id = ?;'''

    cur = conn.cursor()
    cur.execute(sql, id)
    return cur.fetchall()


def get_rowsummary(id):
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        try:
            id = (id,)
            number = find_mysummary(conn, id)
            return number
        except Exception:
            return 'No summary'


if __name__ == '__main__':
    get_rowsummary()