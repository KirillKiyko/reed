import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def get_publications(conn):
    status = ('publish',)

    sql = '''SELECT title, url, photo, keywords, summary, date, status FROM summarization WHERE status = ?'''

    cur = conn.cursor()
    cur.execute(sql, status)

    return cur.fetchall()


def get_all_feeds():
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        data = get_publications(conn)
        return data


if __name__ == '__main__':
    get_all_feeds()