import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def create_new_user(conn, user):
    sql = ''' INSERT INTO user(firstname,secondname,email,password,status,token)
              VALUES(?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, user)


def create_user(firstname, secondname, email, password, token):
    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        status = 'user'
        user_information = (firstname, secondname, email, password, status, token)


        try:
            create_new_user(conn, user_information)
            return 'User created'
        except Exception:
            return 'User exist'


if __name__ == '__main__':
    create_user()
