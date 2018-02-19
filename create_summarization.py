import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def create_summarization(conn, summarization):
    sql = ''' INSERT INTO summarization(url,title,photo,keywords,summary,date,status,user_id)             
              VALUES(?,?,?,?,?,?,?,?)'''

    cur = conn.cursor()
    cur.execute(sql, summarization)

    return cur.lastrowid


def main_summarization(data, id):

    database = "./hashit.db"

    conn = create_connection(database)
    with conn:
        sending_data = (data.get('link'),data.get('title'),data.get('photo'),data.get('keywords'),
                         data.get('summary'),data.get('date'),'undefined', id)

        try:
            number = create_summarization(conn, sending_data)
            return number
        except Exception:
            return 'You have this result'


if __name__ == '__main__':
    main_summarization()