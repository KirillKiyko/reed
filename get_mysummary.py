import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def get_publications(id, conn):

    sql = '''SELECT title, url, photo, keywords, summary, date, status FROM summarization WHERE user_id = ?'''

    cur = conn.cursor()
    cur.execute(sql, id)

    return cur.fetchall()


def get_mysummary(id):
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        id = (id,)
        data = get_publications(id, conn)
        return data


if __name__ == '__main__':
    get_mysummary()