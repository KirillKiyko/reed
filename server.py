import os
import re
import ast
import json
import logging
import tornado.web
import tornado.ioloop
import tornado.httputil
import tornado.auth
import tornado.gen
import tornado.escape

from tornado.escape import json_decode, json_encode
from get_title import get_title
from get_user import get_user
from newspaper import Article
from langdetect import detect
from get_idUser import get_idUser
from get_rownum import get_rownum
from create_user import create_user
from check_token import check_token
from code_for_forgot import code_for_forgot
from check_forgot_user import check_forgot_user
from get_all_feed import get_all_feeds
from get_mysummary import get_mysummary
from change_status import change_status
from change_mobile_status import change_mobile_status
from get_autentificate import check_user
from get_rowsummary import get_rowsummary
from delete_publications import main_delete
from get_users_token import get_users_token
from get_all_dashboards import get_all_dashboards
from get_rowdashboard import get_rowdashboard
from get_tempuser_code import get_tempuser_code
from get_password import get_password
from create_summarization import main_summarization
from push_notification import push_notification
from pass_validation import pass_validation
from send_code import send_code
from update_token import update_token
from update_password import update_password
from hide_block import hide_block


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user.decode('utf-8') != 'support@reedit.io':
            self.redirect('/user_feed')
        else:
            self.render('admin.html')


    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            data = self.get_argument('data')
            data = json.loads(data)

        if data.get('action') == 'load_page':
            full_summarization = get_all_dashboards()

            full = []

            for data in full_summarization:
                full.append(
                    {'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3], 'summary': data[4],
                     'date': data[5]})

            full.reverse()

            number = get_rowdashboard()

            self.write(json.dumps({'summary': full,
                                   'number': number[0][0]}))
        elif data.get('action') == 'publish' or data.get('action') == 'private':
            link = data.get('link')
            print(link)

            id = get_idUser(link)
            print(id)

            id = id[0][0]

            if data.get('action') == 'publish':
                tokens = get_users_token()

                if tokens != []:
                    ids = []

                    for i in tokens:
                        ids.append(i[0])

                    title = get_title(link)

                    result = push_notification(ids, title[0][0])

            change_status(data.get('action'), link, id)
            self.write(json.dumps({'status': 'done'}))


class AdminFeed(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user.decode('utf-8') != 'support@reedit.io':
            self.redirect('/user_feed')
        else:
            self.render('admin_feed.html')

    def post(self):
        try:
            action = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            data = self.get_argument('data')
            data = json.loads(data)

        action = data.get('action')

        if action == 'load_page':
            full_summarization = get_all_feeds()

            full = []

            for data in full_summarization:
                full.append({'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3], 'summary': data[4],
                             'date': data[5]})

            full.reverse()

            number = get_rownum()

            self.write(json.dumps({'summary': full,
                                   'number': number[0][0]}))
        elif action == 'hide':
            link = data.get('link')
            print(link)

            id = get_idUser(link)

            id = id[0][0]
            print(id)

            result = hide_block(link, id)
            print(result)
            self.write(json.dumps({'status': 'done'}))


class MySummary(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user.decode('utf-8') != 'support@reedit.io':
            self.redirect('/user_feed')
        else:
            self.render('summ.html')


    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            data = self.get_argument('data')
            data = json.loads(data)

        action = data.get('action')

        if action == 'load_page':
            email = self.current_user.decode('utf-8')

            id = get_user(email)
            id = id[0][0]


            full_summarization = get_mysummary(id)

            full = []

            for data in full_summarization:
                full.append(
                    {'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3], 'summary': data[4],
                     'date': data[5]})

            full.reverse()

            number = get_rowsummary(id)

            self.write(json.dumps({'summary': full,
                                   'number': number[0][0]}))
        elif action == 'summary':
            try:
                url = json.loads(self.request.body.decode('utf-8'))
            except Exception:
                url = self.get_argument('data')
                url = json.loads(url)

            try:
                url = url.get('url')
                url = re.sub(' ', '', url)

                email = self.current_user.decode('utf-8')

                article = Article(url, language='en')
                article.download()
                article.parse()

                title = article.title

                if detect(title) != 'en' or detect(article.text) != 'en':
                    self.write(json.dumps({'result': 'This language will be supported soon'}))
                else:
                    try:
                        image = article.top_image
                    except Exception:
                        image = ''

                    article.nlp()

                    try:
                        keywords = article.keywords
                        keywords = ','.join(keywords)
                    except Exception:
                        keywords = 'Sorry,no,keywords,found'

                    try:
                        summary = article.summary
                        summary = '<p style = "margin: 10px 0px 10px 0px">' + re.sub(r'\.', r'.</p><p style = "margin: 10px 0px 10px 0px">', summary)
                        summary = summary[:-40]
                    except Exception:
                        summary = 'Sorry, no summmary found'

                    try:
                        publish_date = article.publish_date
                        publish_date = publish_date.date()
                    except Exception:
                        publish_date = 'XII b.c.'

                    id = get_user(email)
                    id = id[0][0]

                    if url[-1] != '/':
                        summarized = {'title': title,
                                      'link': url,
                                      'photo': image,
                                      'keywords': keywords,
                                      'summary': str(summary),
                                      'date': str(publish_date)}
                    else:
                        url = url[:-1]

                        summarized = {'title': title,
                                      'link': url,
                                      'photo': image,
                                      'keywords': keywords,
                                      'summary': str(summary),
                                      'date': str(publish_date)}

                    result = main_summarization(summarized, id)

                    if result == 'You have this result':
                        jsn = {'result': result}
                        self.write(json.dumps(jsn))
                    else:
                        jsn = {'summary': summarized,
                               'number': result,
                               'result': 'done'}

                        self.write(json.dumps(jsn))
            except Exception:
                jsn = {'result': 'This URL is unsummarizable'}
                self.write(json.dumps(jsn))

        elif action == 'delete':
            try:
                url = json.loads(self.request.body.decode('utf-8'))
            except Exception:
                url = self.get_argument('data')
                url = json.loads(url)

            url = url.get('url')

            email = self.current_user.decode('utf-8')

            id = get_user(email)
            id = id[0][0]

            main_delete(id, url)

            self.write(json.dumps({'result': 'done'}))


class RedirectPage(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        page = self.get_argument("page")
        if page == '1':
            self.redirect('/admin')
        elif page == '2':
            self.redirect('/admin_feed')
        elif page == '4':
            self.redirect('/user_feed')
        elif page == '5':
            self.redirect('/user_summary')
        else:
            self.redirect('/summary')


class UserPage(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user.decode('utf-8') == 'support@reedit.io':
            self.redirect('/admin')
        else:
            self.render('user_feed.html')


    def post(self):
        try:
            action = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            action = self.get_argument('data')
            action = json.loads(action)

        action = action.get('action')


        if action == 'load_page':
            full_summarization = get_all_feeds()

            full = []

            for data in full_summarization:
                full.append({'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3], 'summary': data[4],
                             'date': data[5]})

            full.reverse()

            number = get_rownum()

            self.write(json.dumps({'summary': full,
                                   'number': number[0][0]}))


class UserSummary(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        if self.current_user.decode('utf-8') == 'support@reedit.io':
            self.redirect('/admin')
        else:
            self.render('user_summ.html')


    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            data = self.get_argument('data')
            data = json.loads(data)

        action = data.get('action')

        if action == 'load_page':
            email = self.current_user.decode('utf-8')

            id = get_user(email)
            id = id[0][0]


            full_summarization = get_mysummary(id)

            full = []

            for data in full_summarization:
                full.append(
                    {'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3], 'summary': data[4],
                     'date': data[5]})

            full.reverse()

            number = get_rowsummary(id)

            self.write(json.dumps({'summary': full,
                                   'number': number[0][0]}))
        elif action == 'summary':
            try:
                url = json.loads(self.request.body.decode('utf-8'))
            except Exception:
                url = self.get_argument('data')
                url = json.loads(url)

            try:
                url = url.get('url')
                url = re.sub(' ', '', url)

                email = self.current_user.decode('utf-8')

                article = Article(url, language='en')
                article.download()
                article.parse()

                title = article.title

                if detect(title) != 'en' or detect(article.text) != 'en':
                    self.write(json.dumps({'result': 'This language will be supported soon'}))
                else:
                    try:
                        image = article.top_image
                    except Exception:
                        image = ''

                    article.nlp()

                    try:
                        keywords = article.keywords
                        keywords = ','.join(keywords)
                    except Exception:
                        keywords = 'Sorry,no,keywords,found'

                    try:
                        summary = article.summary
                        summary = '<p style = "margin: 10px 0px 10px 0px">' + re.sub(r'\.', r'.</p><p style = "margin: 10px 0px 10px 0px">', summary)
                        summary = summary[:-40]
                    except Exception:
                        summary = 'Sorry, no summmary found'

                    try:
                        publish_date = article.publish_date
                        publish_date = publish_date.date()
                    except Exception:
                        publish_date = 'XII b.c.'

                    if url[-1] == '/':
                        summarized = {'title': title,
                                      'link': url,
                                      'photo': image,
                                      'keywords': keywords,
                                      'summary': str(summary),
                                      'date': str(publish_date)}
                    else:
                        url = url + '/'

                        summarized = {'title': title,
                                      'link': url,
                                      'photo': image,
                                      'keywords': keywords,
                                      'summary': str(summary),
                                      'date': str(publish_date)}

                    id = get_user(email)
                    id = id[0][0]

                    result = main_summarization(summarized, id)

                    summarized = {'title': title,
                                  'link': url,
                                  'photo': image,
                                  'keywords': keywords,
                                  'summary': str(summary),
                                  'date': str(publish_date)}

                    if result == 'You have this result':
                        jsn = {'result': result}
                        self.write(json.dumps(jsn))
                    else:
                        jsn = {'summary': summarized,
                               'number': result,
                               'result': 'done'}

                        self.write(json.dumps(jsn))
            except Exception:
                jsn = {'result': 'This URL is unsummarizable'}
                self.write(json.dumps(jsn))



        elif action == 'delete':
            try:
                url = json.loads(self.request.body.decode('utf-8'))
            except Exception:
                url = self.get_argument('data')
                url = json.loads(url)

            url = url.get('url')

            email = self.current_user.decode('utf-8')

            id = get_user(email)
            id = id[0][0]

            main_delete(id, url)

            self.write(json.dumps({'result': 'done'}))


class MobileFeeds(tornado.web.RequestHandler):
    def get(self):
        if self.current_user:
            if self.current_user.decode('utf-8') == 'support@reedit.io':
                self.redirect('/admin')
            else:
                self.redirect('/user_feed')
        else:
            self.render('index.html')


    def post(self):
        try:
            action = json.loads(self.request.body.decode('utf-8'))

            action = ast.literal_eval(action)
            action = action.get('action')


            if action == 'load_page':
                full_summarization = get_all_feeds()

                full = []

                for data in full_summarization:
                    send_summary = ''
                    for i in range(3):
                        number = i + 1
                        send_summary = send_summary + '<p style = "margin: 10px 0px 10px 0px">' + data[4].split('<p style = "margin: 10px 0px 10px 0px">')[number]

                    full.append(
                        {'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3],
                         'summary': send_summary,
                         'date': data[5]})

                full.reverse()

                number = get_rownum()

                self.write(json.dumps({'summary': full,
                                       'number': number[0][0]}))
        except Exception:
            self.redirect('/user_feed')


class MobileSummary(tornado.web.RequestHandler):
    def get(self):
        if self.current_user:
            if self.current_user.decode('utf-8') == 'support@reedit.io':
                self.redirect('/admin')
            else:
                self.redirect('/user_feed')
        else:
            self.render('index.html')


    def post(self):
        data = json.loads(self.request.body.decode('utf-8'))
        # data = {}
        # tornado.httputil.parse_body_arguments(self.request.headers["Content-Type"], self.request.body, data)
        #
        # logging.getLogger().debug("args={}".format(data))

        action = data.get('action')
        # action = action[0]
        # action = action.decode('utf-8')
        email = data.get('email')
        # email = email[0]
        # email = email.decode('utf-8')

        if action == 'load_page':
            id = get_user(email)
            id = id[0][0]


            full_summarization = get_mysummary(id)

            full = []

            for data in full_summarization:
                send_summary = ''
                print(data[4])
                for i in range(3):
                    number = i + 1
                    send_summary = send_summary + '<p style = "margin: 10px 0px 10px 0px">' + data[4].split('<p style = "margin: 10px 0px 10px 0px">')[number]
                    print(send_summary)

                full.append(
                    {'title': data[0], 'link': data[1], 'photo': data[2], 'keywords': data[3], 'summary': send_summary,
                     'date': data[5]})

            full.reverse()

            self.write(json.dumps({'summary': full}))
        elif action == 'summary':
            try:
                url = data.get('url')
                # url = url[0]
                # url = url.decode('utf-8')

                url = re.sub(' ', '', url)

                article = Article(url, language='en')
                article.download()
                article.parse()

                title = article.title

                if detect(title) != 'en' or detect(article.text) != 'en':
                    self.write(json.dumps({'result': 'This language will be supported soon'}))
                else:
                    try:
                        image = article.top_image
                    except Exception:
                        image = ''

                    article.nlp()

                    try:
                        keywords = article.keywords
                        keywords = ','.join(keywords)
                    except Exception:
                        keywords = 'Sorry,no,keywords,found'

                    try:
                        summary = article.summary
                        summary = '<p style = "margin: 10px 0px 10px 0px">' + re.sub(r'\.', r'.</p><p style = "margin: 10px 0px 10px 0px">', summary)
                        summary = summary[:-40]
                    except Exception:
                        summary = 'Sorry, no summmary found'

                    try:
                        publish_date = article.publish_date
                        publish_date = publish_date.date()
                    except Exception:
                        publish_date = 'XII b.c.'

                    if url[-1] == '/':
                        summarized = {'title': title,
                                      'link': url,
                                      'photo': image,
                                      'keywords': keywords,
                                      'summary': str(summary),
                                      'date': str(publish_date)}
                    else:
                        url = url + '/'

                        summarized = {'title': title,
                                      'link': url,
                                      'photo': image,
                                      'keywords': keywords,
                                      'summary': str(summary),
                                      'date': str(publish_date)}

                    id = get_user(email)
                    id = id[0][0]

                    result = main_summarization(summarized, id)

                    send_summary = ''
                    for i in range(3):
                        number = i + 1
                        send_summary = send_summary + '<p style = "margin: 10px 0px 10px 0px">' + summary.split('<p style = "margin: 10px 0px 10px 0px">')[number]

                    summarized = {'title': title,
                                  'link': url,
                                  'photo': image,
                                  'keywords': keywords,
                                  'summary': send_summary,
                                  'date': str(publish_date)}

                    if result == 'You have this result':
                        jsn = {'result': result}
                        self.write(json.dumps(jsn))
                    else:

                        self.write(json.dumps(summarized))
            except Exception:
                jsn = {'result': 'This URL is unsummarizable'}
                self.write(json.dumps(jsn))

        elif action == 'delete':
            url = data.get('url')

            id = get_user(email)
            id = id[0][0]

            main_delete(id, url)

            self.write(json.dumps({'result': 'done'}))


class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user:
            if self.current_user.decode('utf-8') == 'support@reedit.io':
                self.redirect('/admin')
            else:
                self.redirect('/user_feed')
        else:
            self.render('index.html')


    def post(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            data = self.get_argument('data')
            data = json.loads(data)

        print(data.get('action'))

        if data.get('action') == 'registration':
            name = data.get("name")
            surname = data.get("surname")
            email = data.get("email")
            password = data.get("password")

            validation = pass_validation(password)

            if validation == 'Your password seems fine':
                token = data.get('token')

                if token != None:
                    result = create_user(name, surname, email, password, token)
                else:
                    token = "no_token"

                    result = create_user(name, surname, email, password, token)

                if result == 'User created':
                    self.set_secure_cookie("user", email)

                    self.write(json.dumps({'action': 'redirect',
                                           'email': email}))
                else:
                    self.write(json.dumps({'action': 'Incorrect data'}))
            else:
                self.write(json.dumps({'action': validation}))
        elif data.get('action') == 'login':
            email = data.get("email")
            password = data.get("password")

            gate = check_user(email, password)

            try:
                if gate[0][0] == 'admin':
                    self.set_secure_cookie("user", email)

                    self.write(json.dumps({'action': 'redirect_admin',
                                           'email': email}))
                elif gate[0][0] == 'user':
                    token = data.get('token')

                    if token != None:
                        update_token(token, email)
                    else:
                        result = check_token(email)

                        if result == [] or result[0][0] == "no_token":
                            token = "no_token"

                            update_token(token, email)

                    self.set_secure_cookie("user", email)

                    self.write(json.dumps({'action': 'redirect_user',
                                           'email': email}))
                else:
                    self.write(json.dumps({'action': 'Incorrect email or password'}))
            except Exception:
                self.write(json.dumps({'action': 'Incorrect email or password'}))

        elif data.get('action') == 'forgot_email':
            email = data.get("email")

            email_db = check_forgot_user(email)

            if email_db != []:
                code = send_code(email)
                code_for_forgot(code, email)

                if code == 'Incorrect email':
                    self.write(json.dumps({'action': 'Incorrect email'}))
                else:
                    self.write(json.dumps({'action': 'Code sent'}))
            else:
                self.write(json.dumps({'action': 'Incorrect email'}))

        elif data.get('action') == 'confirm_code':
            email = data.get("email")
            code = data.get('code')
            new_pass = data.get('new_pass')
            confirm_pass = data.get('confirm_pass')

            if new_pass == confirm_pass:
                validation = pass_validation(new_pass)

                if validation == 'Your password seems fine':
                    code_db = get_tempuser_code(email)

                    if code == code_db[0][0]:
                        update_password(new_pass, email)

                        gate = check_user(email, new_pass)

                        if gate[0][0] == 'admin':
                            self.set_secure_cookie("user", email)

                            self.write(json.dumps({'action': 'redirect_admin',
                                                   'email': email}))
                        elif gate[0][0] == 'user':
                            token = data.get('token')

                            if token != None:
                                update_token(token, email)
                            else:
                                result = check_token(email)

                                if result == [] or result[0][0] == "no_token":
                                    token = "no_token"

                                    update_token(token, email)

                            self.set_secure_cookie("user", email)

                            self.write(json.dumps({'action': 'redirect_user',
                                                   'email': email}))
                    else:
                        self.write(json.dumps({'action': 'Incorrect data'}))
                else:
                    self.write(json.dumps({'action': 'Incorrect data'}))
            else:
                self.write(json.dumps({'action': 'Incorrect data'}))


class LogoutHandler(BaseHandler):
    def post(self):
        self.clear_cookie("user")
        self.redirect('login')


class RedirectLogin(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/login')
        else:
            if self.current_user.decode('utf-8') == 'support@reedit.io':
                self.redirect('/admin')
            else:
                self.redirect('/user_feed')


class RedirectLogin2(BaseHandler):
    def get(self):
        if not self.current_user:
            self.redirect('/login')
        else:
            if self.current_user.decode('utf-8') == 'support@reedit.io':
                self.redirect('/admin')
            else:
                self.redirect('/user_feed')


class GoogleOAuth2LoginHandler(tornado.web.RequestHandler,
                               tornado.auth.GoogleOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        print('GET REQUEST')
        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                redirect_uri='http://localhost:8000/google_login',
                code=self.get_argument('code'))
            user = yield self.oauth2_request(
                "https://www.googleapis.com/oauth2/v1/userinfo",
                access_token=access["access_token"])
            user_info = get_user(user['email'])
            if user_info == []:
                token = 'no_token'
                password = None
                create_user(user['given_name'], user['family_name'], user['email'], password, token)
                self.set_secure_cookie('user', user['email'])
                self.redirect('user_feed')
            else:
                if user['email'] == 'reedautoreply@gmail.com':
                    self.set_secure_cookie('user', 'support@reedit.io')
                    self.redirect('admin')
                else:
                    self.set_secure_cookie('user', user['email'])
                    self.redirect('user_feed')
        else:
            self.authorize_redirect(
                redirect_uri='http://localhost:8000/google_login',
                client_id=self.settings['google_oauth']['key'],
                client_secret=self.settings['google_oauth']['secret'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'})


class TwitterLoginHandler(tornado.web.RequestHandler,
                          tornado.auth.TwitterMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument('oauth_token', None):
            user = yield self.get_authenticated_user(
                include_email=True
            )
            print(user['name'])
            print(user['email'])
            # self.set_secure_cookie('user', user['email'])
            # self.redirect(self.get_argument('next', '/'))
        else:
            yield self.authorize_redirect(
                callback_uri='http://localhost:8000/twitter_login',
                extra_params={'scope': 'email'})


class FacebookGraphLoginHandler(tornado.web.RequestHandler,
                                tornado.auth.FacebookGraphMixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_argument("code", False):
            access = yield self.get_authenticated_user(
                redirect_uri='http://localhost:8000/facebook_login',
                client_id=self.settings["facebook_api_key"],
                client_secret=self.settings["facebook_secret"],
                code=self.get_argument("code"))
            user = yield self.oauth2_request(
                "https://graph.facebook.com/v2.5/me",
                fields='email,first_name,last_name',
                access_token=access["access_token"])
            user_info = get_user(user['email'])
            if user_info == []:
                token = 'no_token'
                password = None
                create_user(user['first_name'], user['last_name'], user['email'], password, token)
                self.set_secure_cookie('user', user['email'])
                self.redirect('user_feed')
            else:
                if user['email'] == 'reedautoreply@gmail.com':
                    self.set_secure_cookie('user', 'support@reedit.io')
                    self.redirect('admin')
                else:
                    self.set_secure_cookie('user', user['email'])
                    self.redirect('user_feed')
        else:
            yield self.authorize_redirect(
                redirect_uri='http://localhost:8000/facebook_login',
                client_id=self.settings["facebook_api_key"],
                extra_params={"scope": "email,public_profile"})


class PrivacyPolicy(tornado.web.RequestHandler):
    def get(self):
        self.render('privacypolicy.htm')


class TermsOfService(tornado.web.RequestHandler):
    def get(self):
        self.render('terms.htm')


class GoogleVerify(tornado.web.RequestHandler):
    def get(self):
        self.render('google5d453b36b6a0dd4e.html')



settings = {'static_path': os.path.join(os.path.dirname(__file__), "static"),
            'debug': True,
            'serve_traceback': True,
            "login_url": "/login"
}

application = tornado.web.Application([
    (r"/admin", MainHandler),
    (r"/admin_feed", AdminFeed),
    (r"/summary", MySummary),
    (r"/page", RedirectPage),
    (r"/user_feed", UserPage),
    (r"/mobile_feeds", MobileFeeds),
    (r"/user_summary", UserSummary),
    (r"/mobile_summary", MobileSummary),
    (r"/login", LoginHandler),
    (r'/logout', LogoutHandler),
    (r"/google_login", GoogleOAuth2LoginHandler),
    (r"/twitter_login", TwitterLoginHandler),
    (r"/facebook_login", FacebookGraphLoginHandler),
    (r"/privacy_policy", PrivacyPolicy),
    (r"/termsofservice", TermsOfService),
    (r"/google5d453b36b6a0dd4e.html", GoogleVerify),
    (r"/", RedirectLogin),
    (r"", RedirectLogin2),
], cookie_secret="61oETzKTQAGaZdkL5gEmGeJHFuYh7EQnp5XdTP1o/Vo=", **settings)


if __name__ == "__main__":
    application.listen(8000)
    tornado.ioloop.IOLoop.current().start()

# 34.214.238.217
