import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def delete_publication(conn, sending_data):
    sql = '''DELETE FROM summarization WHERE user_id = ? AND url = ?'''

    cur = conn.cursor()
    cur.execute(sql, sending_data)
    conn.commit()
    if cur:
        cur.close()


def main_delete(user_id, url):

    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        sending_data = (user_id, url)
        delete_publication(conn, sending_data)
        return 'Deleted'


if __name__ == '__main__':
    main_delete()