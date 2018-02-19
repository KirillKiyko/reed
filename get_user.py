import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def find_user(conn, email):
    sql = '''SELECT user.id FROM user WHERE email = ? '''

    cur = conn.cursor()
    cur.execute(sql, email)
    user_id = cur.fetchall()
    return user_id


def get_user(email):
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        user_email = [email]
        try:
            user_id = find_user(conn, user_email)
            return user_id
        except Exception:
            return 'No user with this email'


if __name__ == '__main__':
    get_user()