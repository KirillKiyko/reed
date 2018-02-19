import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def get_notification(link, conn):

    sql = '''SELECT title, photo, keywords, summary, date FROM summarization WHERE url = ?'''

    cur = conn.cursor()
    cur.execute(sql, link)

    return cur.fetchall()


def get_new_publish(link):
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        link = (link,)
        data = get_notification(link, conn)
        return data


if __name__ == '__main__':
    get_new_publish()