import sqlite3
import re
import requests
import Identifai.Identifai
import oauth2



from sqlite3 import Error

def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


def get_users_token():
    database = "./hashit.db"
    conn = create_connection(database)
    cursor = conn.cursor()

    # cursor.execute('DELETE FROM user WHERE email="kijko97@gmail.com"')
    # conn.commit()

    cursor.execute('SELECT * FROM user WHERE email="kijko97@gmail.com"')
    ids = cursor.fetchall()
    print(ids)

get_users_token()


# def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
#     consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
#     token = oauth2.Token(key=key, secret=secret)
#     client = oauth2.Client(consumer, token)
#     resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
#     return content
#
#
# CONSUMER_KEY = 'jsqQ66gnLCKmLxR6NcNeR2i1L'
# CONSUMER_SECRET = 'kR8OFIRT1vwBIB678Kq0J220QaeH8hDNj9dsqStvkLKCSid2Rd'
# home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', 'abcdefg', 'hijklmnop' )
# print(home_timeline)
