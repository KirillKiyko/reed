import sqlite3

from sqlite3 import Error


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def create_table(conn, hashit_tables):
    try:
        cursor = conn.cursor()
        cursor.execute(hashit_tables)
    except Error as e:
        print(e)


def main():
    database = './hashit.db'

    hashit_summarization = '''CREATE TABLE
                              IF NOT EXISTS summarization (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                title text,
                                url text,
                                photo text,
                                keywords text,
                                summary text,
                                date date,
                                status text,
                                user_id integer,
                                FOREIGN KEY (user_id) REFERENCES user (id),
                                UNIQUE (url, user_id));'''

    hashit_users = '''CREATE TABLE
                      IF NOT EXISTS user (
                       id integer PRIMARY KEY AUTOINCREMENT,
                       firstname text,  
                       secondname text,
                       email text,
                       password text,
                       status text, 
                       token text,    
                       code text,         
                       UNIQUE (email));'''
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, hashit_summarization)
        create_table(conn, hashit_users)
    else:
        print('u r noob')


if __name__ == '__main__':
    main()