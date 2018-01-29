from classification.sessionutils import get_session_from_token, \
    SavedTokenError, get_new_session, save_token
from oauthlib.oauth2 import TokenExpiredError
from requests.auth import HTTPBasicAuth


class Classification:

    AUTHORIZE_URL = 'https://auth.fit.cvut.cz/oauth/authorize'
    TOKEN_URL = 'https://auth.fit.cvut.cz/oauth/token'

    API_URL = 'https://rozvoj.fit.cvut.cz/evolution-dev/' \
              'classification-dev/api/v1'

    def __init__(self, client_id, client_secret,
                 callback_host='localhost', callback_port=8080,
                 force_new_token=False):

        self.session = None
        self.client_id = client_id
        self.client_secret = client_secret

        self.reinit_session(client_id, client_secret, callback_host,
                            callback_port, force_new_token)

    def reinit_session(self, client_id, client_secret,
                       callback_host, callback_port,
                       force_new_token):

        if not force_new_token:
            try:
                self.session = get_session_from_token(client_id,
                                                      client_secret,
                                                      callback_host,
                                                      callback_port,
                                                      self.TOKEN_URL)
                return
            except SavedTokenError:
                pass

        if self.session is None:

            self.session = get_new_session(client_id, client_secret,
                                           callback_host, callback_port,
                                           self.AUTHORIZE_URL,
                                           self.TOKEN_URL)
            # self.session.refresh_token(self.TOKEN_URL,
            #                            refresh_token=self.session.token['refresh_token'],
            #                            auth=HTTPBasicAuth(self.client_id, self.client_secret))

    def drop_session(self):
        self.session.close()
        self.session = None

    def refresh_token(fun):
        def inner(self, *args, **kwargs):
            try:
                return fun(self, *args, **kwargs)

            except TokenExpiredError:
                # If the token is expired - get a new one and try again
                r_token = self.session.token['refresh_token']
                auth = HTTPBasicAuth(self.client_id, self.client_secret)
                token = self.session.refresh_token(self.TOKEN_URL,
                                                   refresh_token=r_token,
                                                   auth=auth)
                self.session.token = token
                save_token(token)
                return fun(self, *args, **kwargs)

        return inner

    @refresh_token
    def find_student_classification(self, course_code, student_username,
                                    **kwargs):
        return self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/student-classifications'
                                f'/{student_username}',
                                **kwargs)
