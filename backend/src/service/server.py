import cgi
from http import HTTPStatus
import json
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime
from uuid import uuid1
from copy import deepcopy
import sys

sys.path.append('/code/src/dao')

FILE_NAME = f'{datetime.now().strftime("reddit-%Y%m%d%H%M")}.txt'
MODE = None


class Server(BaseHTTPRequestHandler):
    """Class implementing REST service"""

    def __init__(self, request, client_address, server):
        self.mode = MODE

        if self.mode == "mongo":
            from database_mongo import get_json
        elif self.mode == "postgres":
            from database_postgres import get_json

        self.jsn, self.unique, self.u_id, self.file = get_json()
        self.keys = ["author", "post_date", "post_url", "number_of_comments", "number_of_votes", "post_category",
                     "user_karma", "user_comment_karma", "post_karma", "user_cake_day"]

        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _set_create_response(self):
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def _set_bad_response(self):
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def data_POST(self):
        """Read the json data"""

        ctype, pdict = cgi.parse_header(self.headers['content-type'])

        if ctype != 'application/json':
            self._set_bad_response()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        return message

    def data_GET(self):
        """Return response by UUID"""
        self.jsn = self.jsn.split("}")

        for index, item in enumerate(self.u_id):
            if item == self.path.split("/")[2]:
                self.jsn = self.jsn[index][1:] + "}" + "\n"
                response = bytes(self.jsn, "utf-8")

        return response

    def form_POST(self, message):
        """Create data row in file"""

        result = [uuid1().hex]
        keys = self.keys

        flag = False

        for i in range(0, len(keys)):
            for key, value in message.items():
                if keys[i] == key:
                    result.append(value)
                    flag = True

            if not flag:
                result.append(";")

        while len(keys) != len(result) - 1:
            result.append(";")

        return result

    def form_PUT(self, message, uid):
        """Form data Put req"""
        keys = {}

        for i in self.file:
            if i["uid"] == uid:
                keys = i

        copykeys = deepcopy(keys)

        for key, value in keys.items():
            for k, v in message.items():
                if k == key:
                    copykeys[key] = v

        return copykeys

    def form_PAGINATION(self, path, mode):
        NUMBER_OF_POSTS = 10
        paggination_query = path.split('=')[1].strip('/')
        if 'post_date' or 'number_of_votes' or 'post_category' in paggination_query:
            paggination_query = paggination_query.split('&')[0]

        paggination_query = int(paggination_query)

        response = []

        try:
            if paggination_query != 0:
                for i in range(NUMBER_OF_POSTS * paggination_query, NUMBER_OF_POSTS*paggination_query+NUMBER_OF_POSTS):
                    response.append(self.file[i])
            else:
                for i in range(0, NUMBER_OF_POSTS):
                    response.append(self.file[i])
        except IndexError:
            pass

        if mode == 'filter':
            return response
        else:
            return json.dumps(response)

    def form_FILTER(self, path, response=[]):
        filter_query = path.split('=')[-1].strip('/')
        result = []

        if not response:
            response = self.file

        if 'post_date' in path:
            for i in response:
                if i['post_date'] == filter_query:
                    result.append(i)

        if 'number_of_votes' in path:
            for i in response:
                if i['number_of_votes'] == filter_query:
                    result.append(i)

        if 'post_category' in path:
            for i in response:
                if i['post_category'] == filter_query:
                    result.append(i)

        return json.dumps(result)

    def do_GET(self):
        if self.path == "/posts/":
            """GET all data"""
            self._set_response()
            response = bytes(self.jsn, "utf-8")
            self.wfile.write(response)
        elif self.path in self.unique:
            """GET by unique_id"""
            self._set_response()
            response = self.data_GET()
            self.wfile.write(response)
        elif "page" in self.path:
            """Pagination"""
            self._set_response()
            filters = ["post_date" , "number_of_votes" , "post_category"]
            if [x for x in filters if x in self.path]:
                """Filter"""
                response = self.form_PAGINATION(self.path, 'filter')
                response = self.form_FILTER(self.path, response)
                response = bytes(response, "utf-8")
                self.wfile.write(response)
            else:
                response = self.form_PAGINATION(self.path, 'nofilter')
                response = bytes(response, "utf-8")
                self.wfile.write(response)
        elif "post_date" or "numer_of_votes" or "post_category" in self.path:
            """Filter"""
            self._set_response()
            response = self.form_FILTER(self.path)
            response = bytes(response, "utf-8")
            self.wfile.write(response)

    def do_POST(self):
        """POST new data"""

        if self.path == "/posts/":
            try:
                self._set_create_response()
                message = self.data_POST()
                post_message = self.form_POST(message)

                if self.mode == 'postgres':
                    from database_postgres import write_in_database
                elif self.mode == 'mongo':
                    from database_mongo import write_in_database

                write_in_database(post_message)
            except Exception:
                self._set_bad_response()
        else:
            self._set_response()

    def do_DELETE(self):
        """DELETE by unique id"""

        if self.path in self.unique:
            self._set_response()

            if self.mode == 'postgres':
                from database_postgres import delete_data
            elif self.mode == 'mongo':
                from database_mongo import delete_data

            delete_data(self.path.split('/')[2])
        else:
            self._set_bad_response()

    def do_PUT(self):
        """Update existing data by unique id"""

        if self.path in self.unique:
            self._set_create_response()

            message = self.data_POST()
            result = self.form_PUT(message, self.path.split("/")[2])

            if self.mode == 'postgres':
                from database_postgres import update_data
            elif self.mode == 'mongo':
                from database_mongo import update_data

            update_data(**result)
        else:
            self._set_bad_response()


def run(mode, server_class=HTTPServer, request_handler=Server, port=8080):
    """Run the server"""
    try:
        print("Starting the server... \nPlease, do the GET request.")

        global MODE
        MODE = mode

        server_address = ('', port)
        httpd = server_class(server_address, request_handler)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print(HTTPStatus.SERVICE_UNAVAILABLE)
        httpd.server_close()
    except:
        print(HTTPStatus.INTERNAL_SERVER_ERROR)