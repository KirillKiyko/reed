import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def autentificate_user(conn, user_information):
    sql = '''SELECT status FROM user WHERE email = ? AND password = ? '''

    cur = conn.cursor()
    cur.execute(sql, user_information)
    user_status = cur.fetchall()
    return user_status


def check_user(email, password):
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        user_information = (email, password)

        try:
            user_status = autentificate_user(conn, user_information)
            return user_status
        except Exception:
            return [('Incorrect data or user not exist'),]


if __name__ == '__main__':
    check_user()