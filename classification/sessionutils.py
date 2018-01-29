import json
import os.path
from http import server
from oauthlib.oauth2 import WebApplicationClient
from requests_oauthlib import OAuth2Session
import webbrowser
from .exceptions import SavedTokenError, AuthError
from urllib.parse import urlparse, parse_qs


TOKEN_FILE_NAME = 'saved_token'


def get_session_from_token(client_id, client_secret,
                           callback_host, callback_port,
                           token_url):
    if not os.path.isfile(TOKEN_FILE_NAME):
        raise SavedTokenError('File does not exist')

    token = None

    try:
        with open(TOKEN_FILE_NAME, 'r') as f:
            token = json.load(f)

    except Exception as e:
        raise SavedTokenError(f'Error reading token from file: {e}')

    if 'access_token' not in token \
            or 'refresh_token' not in token:
        raise SavedTokenError('Invalid format: '
                              'missing some required fields - '
                              'access_token, refresh_token and '
                              'must be provided')

    callback_url = make_callback_url(callback_host, callback_port)

    session = OAuth2Session(client_id=client_id,
                            token=token,
                            redirect_uri=callback_url)

    return session


def save_token(token):
    with open(TOKEN_FILE_NAME, 'w') as f:
        json.dump(token, f)


def get_new_session(client_id, client_secret,
                    callback_host, callback_port,
                    auth_url, token_url):
    callback_url = make_callback_url(callback_host, callback_port)

    code = ''

    class CodeHandler(server.BaseHTTPRequestHandler):

        def do_GET(self):
            nonlocal code

            parsed = urlparse(self.path)
            query = parse_qs(parsed.query)

            if 'code' not in query:
                raise AuthError('\'code\' query parameter '
                                'is missing in response')

            code = query['code'][0]

    # init OAuth client
    client = WebApplicationClient(client_id=client_id)
    request_uri = client.prepare_request_uri(auth_url,
                                             redirect_uri=callback_url)

    webbrowser.open(request_uri, new=1)

    # init server and get code
    httpd = server.HTTPServer((callback_host, callback_port), CodeHandler)
    httpd.handle_request()

    session = OAuth2Session(client_id=client_id,
                            redirect_uri=callback_url)

    session.fetch_token(token_url=token_url, client_id=client_id, client_secret=client_secret, code=code)

    save_token(session.token)

    return session


def make_callback_url(callback_host, callback_port):
    return f'http://{callback_host}:{callback_port}'
