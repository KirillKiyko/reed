import tornado.httpclient

http_client = tornado.httpclient.HTTPClient()
cookie = {"Cookie" : 'my_cookie=user'}
http_client.fetch("http://localhost:8888/user_feed",
                  headers=cookie)