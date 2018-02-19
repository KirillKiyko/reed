import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def set_status(conn, sending_data):
    sql = '''UPDATE summarization SET status = ? WHERE url = ? AND user_id = ?;'''

    cur = conn.cursor()
    cur.execute(sql, sending_data)


def change_status(status, url, user_id):

    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        sending_data = (status, url, user_id)
        print(sending_data)

        set_status(conn, sending_data)
        return 'Changed'


if __name__ == '__main__':
    change_status()

# change_status('undefined', 'https://techcrunch.com/2017/10/24/tesla-makes-quick-work-of-puerto-rico-hospital-solar-power-relief-project/', 4)