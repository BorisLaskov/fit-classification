from classification.sessionutils import get_session_from_token, \
    SavedTokenError, get_new_session, save_token
from classification.utils import make_dict_body, \
    get_body_or_raise_error
from classification.payloadconverters \
    import save_request_from_s2t, save_request_from_t2s, \
    s2t_from_get_response, t2s_from_get_response
from classification.types import DictOrNone, ClassificationDtoType, \
    ParseAllDtoType, ParseDtoType, SettingsDtoType, \
    CourseSettingsDtoType, StudentClassificationDtoType, \
    StudentsToTasksType, TasksToStudentsType
from oauthlib.oauth2 import TokenExpiredError
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from functools import wraps


class Classification:
    """The main class for working with Classification API.

    This class has a method for every URL listed in API
    documentation of Classification portal. It also
    manages acquiring and refreshing of the access token.

    See Also:
        :py:class:`~.classificationproxy.ClassificationParamsProxy`
        is a proxy for this class that takes care of saving
        some frequently used parameters.

    Note:
        In order to use this class, you will need to get
        a client ID and Secret codes. You will receive them once
        you register a new application in the
        `AppsManager <https://auth.fit.cvut.cz/manager/>`__.
        Create a new web application there. As the callback URL,
        please put the URL of your local server to catch
        the authorization callback (it is localhost:8080 by default).

    Attributes:
        AUTHORIZE_URL (str): Used to build a login URL to be opened
            in browser.
        TOKEN_URL (str): This endpoint is used to ask the server
            to give and refresh the access token.
        API_URL (str): The base part of the API URL (used in
            every method/API call).
        session (requests_oauthlib.OAuth2Session): This session
            is used to acquire/refresh token and to make API calls.
            Can be passed through the constructor, but it was
            made possible for the purpose of testing; do not pass
            it in for the regular usage.
        client_id (str): A special ID you get when you register
            your application in the
            `AppsManager <https://auth.fit.cvut.cz/manager/>`__.
        client_secret (str): A special secret code you get
            when you register your application in the
            `AppsManager <https://auth.fit.cvut.cz/manager/>`__.

    """

    AUTHORIZE_URL = 'https://auth.fit.cvut.cz/oauth/authorize'
    TOKEN_URL = 'https://auth.fit.cvut.cz/oauth/token'

    API_URL = 'https://rozvoj.fit.cvut.cz/evolution-dev/' \
              'classification-dev/api/v1'

    def __init__(self, client_id: str, client_secret: str,
                 callback_host: str='localhost', callback_port: int=8080,
                 force_new_token: bool=False, session: OAuth2Session=None):
        """Creates a new instance of the library with a new session.

        Initially needed to create a new session, client ID
        and Secret values are stored inside to refresh
        expired access token later.

        Args:
            client_id: A special ID you get when you register
                your application in the
                `AppsManager <https://auth.fit.cvut.cz/manager/>`__.
            client_secret: A special secret code you get
                when you register your application in the
                `AppsManager <https://auth.fit.cvut.cz/manager/>`__.
            callback_host: The host which should
                receive the authorization callback. Used to
                temporarily create a web server in this app
                to get callback with authorization code.
                Defaults to 'localhost'.
            callback_port: The port used together
                with the host described above. Defaults to 8080.
            force_new_token: If True, the login
                process will be initiated again, even if we have
                token saved. Defaults to False.
            session: This session
                is used to acquire/refresh token and to make API calls.
                Can be passed through the constructor, but it was
                made possible for the purpose of testing; do not pass
                it in for the regular usage.

        """

        self.session = None
        self.client_id = client_id
        self.client_secret = client_secret

        # Note that session injection is used primarily for testing purposes
        # You will still need client_id and _secret values for token refresh
        if session is None:
            self.reinit_session(callback_host, callback_port, force_new_token)
        else:
            self.session = session

    def reinit_session(self, callback_host: str='localhost',
                       callback_port: int=8080,
                       force_new_token: bool=False) -> None:
        """Establishes a new session.

        Called by the constructor internally. Use it, for example,
        when you need to log in with different credentials
        (name and password).

        Args:
            callback_host: See
                :py:meth:`~.classification.Classification.__init__`.
            callback_port: See
                :py:meth:`~.classification.Classification.__init__`.
            force_new_token: See
                :py:meth:`~.classification.Classification.__init__`.

        """

        if not force_new_token:
            try:
                self.session = get_session_from_token(self.client_id,
                                                      self.client_secret,
                                                      callback_host,
                                                      callback_port,
                                                      self.TOKEN_URL)
                return
            except SavedTokenError:
                pass

        if self.session is None:

            self.session = get_new_session(self.client_id, self.client_secret,
                                           callback_host, callback_port,
                                           self.AUTHORIZE_URL,
                                           self.TOKEN_URL)

    def drop_session(self) -> None:
        """Closes and deletes internal OAuth2 session."""
        self.session.close()
        self.session = None

    def refresh_token(fun):
        """A decorator used internally to refresh token.

        It is used with functions that make API calls.
        If it captures an error showing that token has
        expired, it tries to refresh it and then
        calls the function that caused it again.

        """
        @wraps(fun)
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

    # -----------------------------------------------
    # ---------- CLASSIFICATION CONTROLLER ----------
    # -----------------------------------------------
    @refresh_token
    def delete_classification(self, course_code: str, classification_id: str,
                              semester: str=None, **kwargs) -> DictOrNone:
        """Deletes classification.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            classification_id: Classification identifier.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`delete` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'classification-identifier': classification_id,
                  'semester': semester}

        resp = self.session.delete(f'{self.API_URL}/public'
                                   f'/courses/{course_code}'
                                   f'/classifications',
                                   params=params, **kwargs)

        return get_body_or_raise_error(resp, 204)

    @refresh_token
    def find_classifications_for_course(self, course_code: str,
                                        semester: str=None, lang: str=None,
                                        **kwargs) -> DictOrNone:
        """Finds classification for the given course.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            semester: Semester identifier.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/classifications',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def save_classification(self, course_code: str,
                            classification_dto: ClassificationDtoType=None,
                            **kwargs) -> DictOrNone:
        """Saves classification for the given course.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            classification_dto: The body for the request. Can be
                a plain Python dictionary or a
                :py:class:`~.entities.ClassificationDto`.
            **kwargs: Anything that :py:func:`post` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        body = make_dict_body(classification_dto)

        resp = self.session.post(f'{self.API_URL}/public'
                                 f'/courses/{course_code}'
                                 f'/classifications',
                                 json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def change_order_of_classifications(self, course_code: str, indexes: dict,
                                        semester: str=None,
                                        **kwargs) -> DictOrNone:
        """Changes the order of classifications.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            indexes: The body for the request. Should be
                a plain Python dictionary.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params`` and ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester}

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/classifications/order',
                                params=params, json=indexes,
                                **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def find_classification(self, course_code: str, identifier: str,
                            semester: str=None,
                            lang: str=None, **kwargs) -> DictOrNone:
        """Finds classification by identifier.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            identifier: Classification identifier.
            semester: Semester identifier.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/classifications/{identifier}',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def clone_classification_definitions(self, target_semester: str,
                                         target_course_code: str,
                                         source_semester: str,
                                         source_course_code: str,
                                         remove_existing: bool,
                                         **kwargs) -> DictOrNone:
        """Clones the definitions of the classification.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            target_semester: Target semester code.
            target_course_code: Target course code.
            source_semester: Source semester code.
            source_course_code: Source course code.
            remove_existing: Remove existing definitions.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'target-semester': target_semester,
                  'source-semester': source_semester,
                  'remove-existing': remove_existing}

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/courses/{source_course_code}'
                                f'/classifications'
                                f'/clones/{target_course_code}',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 201)

    # -----------------------------------------------
    # -------------- EDITOR CONTROLLER --------------
    # -----------------------------------------------
    @refresh_token
    def get_editors(self, course_code: str, **kwargs) -> DictOrNone:
        """Get editors.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}/editors',
                                **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def delete_editor(self, course_code: str, username: str,
                      **kwargs) -> DictOrNone:
        """Delete given editor.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            username: Username of the editor.
            **kwargs: Anything that :py:func:`delete` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.delete(f'{self.API_URL}/public'
                                   f'/courses/{course_code}'
                                   f'/editors/{username}',
                                   **kwargs)

        return get_body_or_raise_error(resp, 204)

    @refresh_token
    def add_editor(self, course_code: str, username: str,
                   **kwargs) -> DictOrNone:
        """Add a new editor.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            username: Username of the editor.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.
        """

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/editors/{username}',
                                **kwargs)

        return get_body_or_raise_error(resp, 201)

    # -----------------------------------------------
    # ------------ EXPRESSION CONTROLLER ------------
    # -----------------------------------------------
    @refresh_token
    def evaluate_all(self, expressions_dto: ParseAllDtoType=None,
                     **kwargs) -> DictOrNone:
        """Evaluate all expressions.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            expressions_dto: The body for the request. Can be
                a plain Python dictionary or a
                :py:class:`~.entities.ExpressionParseAllRequestDto`.
            **kwargs: Anything that :py:func:`post` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        body = make_dict_body(expressions_dto)

        resp = self.session.post(f'{self.API_URL}/public'
                                 f'/course-expressions/analyses',
                                 json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def try_validity(self, expression_dto: ParseDtoType=None,
                     **kwargs) -> DictOrNone:
        """Try validity of an expression.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            expression_dto: The body for the request. Can be
                a plain Python dictionary or a
                :py:class:`~.entities.ExpressionParseRequestDto`.
            **kwargs: Anything that :py:func:`post` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        body = make_dict_body(expression_dto)

        resp = self.session.post(f'{self.API_URL}/public'
                                 f'/expressions/analyses',
                                 json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def get_functions(self, **kwargs) -> DictOrNone:
        """Get all functions.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/expressions/functions',
                                **kwargs)

        return get_body_or_raise_error(resp, 200)

    # -----------------------------------------------
    # ----------- NOTIFICATION CONTROLLER -----------
    # -----------------------------------------------
    @refresh_token
    def get_all_notifications(self, username: str, count: int=None,
                              page: int=None, lang: str=None,
                              **kwargs) -> DictOrNone:
        """Get all notifications.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            username: The name of the user.
            count: Count.
            page: Page.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'count': count, 'page': page, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/notifications/{username}/all',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def get_unread_notifications(self, username: str, count: int=None,
                                 page: int=None, lang: str=None,
                                 **kwargs) -> DictOrNone:
        """Get all unread notifications.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            username: The name of the user.
            count: Count.
            page: Page.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'count': count, 'page': page, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/notifications/{username}/new',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def unread_all_notifications(self, username: str,
                                 **kwargs) -> DictOrNone:
        """Mark all notifications unread.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            username: The name of the user.
            **kwargs: Anything that :py:func:`delete` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.delete(f'{self.API_URL}/public'
                                   f'/notifications/{username}/read',
                                   **kwargs)

        return get_body_or_raise_error(resp, 204)

    @refresh_token
    def read_all_notifications(self, username: str,
                               **kwargs) -> DictOrNone:
        """Mark all notifications read.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            username: The name of the user.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/notifications/{username}/read',
                                **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def unread_notification(self, username: str, id: int,
                            **kwargs) -> DictOrNone:
        """Mark a single notification as unread.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            username: The name of the user.
            id: The identifier of the notification.
            **kwargs: Anything that :py:func:`delete` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.delete(f'{self.API_URL}/public'
                                   f'/notifications/{username}/read/{id}',
                                   **kwargs)

        return get_body_or_raise_error(resp, 204)

    @refresh_token
    def read_notification(self, username: str, id: int,
                          **kwargs) -> DictOrNone:
        """Mark a single notification as read.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            username: The name of the user.
            id: The identifier of the notification.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/notifications/{username}/read/{id}',
                                **kwargs)

        return get_body_or_raise_error(resp, 201)

    # -----------------------------------------------
    # ------------- SETTINGS CONTROLLER -------------
    # -----------------------------------------------
    @refresh_token
    def get_settings(self, semester: str=None, lang: str=None,
                     **kwargs) -> DictOrNone:
        """Get settings.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            semester: Semester identifier.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/settings/my',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def save_my_settings(self, user_settings_dto: SettingsDtoType=None,
                         **kwargs) -> DictOrNone:
        """Save my settings.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            user_settings_dto: The body of the request. Can be
                a plain Python dictionary or a
                :py:class:`~.entities.UserSettingsDto`.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        body = make_dict_body(user_settings_dto)

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/settings/my', json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def save_student_course_settings(
            self, user_course_settings_dto: CourseSettingsDtoType=None,
            semester: str=None, **kwargs) -> DictOrNone:
        """Save student course settings.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            user_course_settings_dto: The body of the request. Can be
                a plain Python dictionary or a
                :py:class:`~.entities.UserCourseSettingsDto`.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params`` and ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester}

        body = make_dict_body(user_course_settings_dto)

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/settings/my/student/courses',
                                params=params, json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    @refresh_token
    def save_teacher_course_settings(
            self, user_course_settings_dto: CourseSettingsDtoType=None,
            semester: str=None, **kwargs):
        """Save teacher course settings.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            user_course_settings_dto: The body of the request. Can be
                a plain Python dictionary or a
                :py:class:`~.entities.UserCourseSettingsDto`.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params`` and ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester}

        body = make_dict_body(user_course_settings_dto)

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/settings/my/teacher/courses',
                                params=params, json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    # -----------------------------------------------
    # ------ STUDENT CLASSIFICATION CONTROLLER ------
    # -----------------------------------------------
    @refresh_token
    def find_student_group_classifications(self, course_code: str,
                                           group_code: str='ALL',
                                           semester: str=None,
                                           **kwargs) -> DictOrNone:
        """Find student group classifications.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            group_code: The code of the group.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/group/{group_code}'
                                f'/student-classifications',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    def find_student_group_classifications_simple_s2t(
            self, course_code: str, group_code: str='ALL',
            semester: str=None, **kwargs) -> DictOrNone:
        """Find student group classifications with a simplified response.

        See :ref:`simplified_operations` section as well as
        :py:meth:`~.find_student_group_classifications` method.

        Args:
            course_code: The code of the course.
            group_code: The code of the group.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the simplified response body
            or ``None``, if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp_body = self.find_student_group_classifications(
            course_code, group_code, semester, **kwargs)

        if resp_body is not None:
            return s2t_from_get_response(resp_body)
        else:
            return None

    def find_student_group_classifications_simple_t2s(
            self, course_code: str, group_code: str='ALL',
            semester: str=None, **kwargs) -> DictOrNone:
        """Find student group classifications with a simplified response.

        See :ref:`simplified_operations` section as well as
        :py:meth:`~.find_student_group_classifications` method.

        Args:
            course_code: The code of the course.
            group_code: The code of the group.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the simplified response body
            or ``None``, if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        resp_body = self.find_student_group_classifications(
            course_code, group_code, semester, **kwargs)

        if resp_body is not None:
            return t2s_from_get_response(resp_body)
        else:
            return None

    @refresh_token
    def find_student_classifications_for_definitions(
            self, course_code: str, identifier: str, group_code: str='ALL',
            semester: str=None, **kwargs) -> DictOrNone:
        """Find student classification for definitions.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            identifier: Classification identifier.
            group_code: The code og the group.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/group/{group_code}'
                                f'/student-classifications/{identifier}',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    @refresh_token
    def save_student_classifications(
            self, course_code: str,
            student_classifications: StudentClassificationDtoType=None,
            semester: str=None, **kwargs) -> DictOrNone:
        """Save student classifications.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            student_classifications: The body of the request. Can be
                a list of plain Python dictionaries or of
                :py:class:`~.entities.StudentClassificationPreviewDto`.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params`` and ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester}

        if student_classifications is not None:
            body = [make_dict_body(s) for s in student_classifications]
        else:
            body = list()

        resp = self.session.put(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/student-classifications',
                                params=params, json=body, **kwargs)

        return get_body_or_raise_error(resp, 201)

    def save_student_classifications_simple_s2t(
            self, course_code: str,
            student_to_tasks: StudentsToTasksType=None,
            semester: str=None, **kwargs) -> DictOrNone:
        """A simplified solution to save students' classifications.

        See :ref:`simplified_operations` section as well as
        :py:meth:`~.save_student_classifications` method.

        Args:
            course_code: The code of the course.
            student_to_tasks: The body of the request.
                See :ref:`simplified_operations` section
                for the format.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params`` and ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        dtos = save_request_from_s2t(student_to_tasks)
        return self.save_student_classifications(course_code, dtos,
                                                 semester, **kwargs)

    def save_student_classifications_simple_t2s(
            self, course_code: str,
            task_to_students: TasksToStudentsType=None,
            semester: str=None, **kwargs) -> DictOrNone:
        """A simplified solution to save students' classifications.

        See :ref:`simplified_operations` section as well as
        :py:meth:`~.save_student_classifications` method.

        Args:
            course_code: The code of the course.
            task_to_students: The body of the request.
                See :ref:`simplified_operations` section
                for the format.
            semester: Semester identifier.
            **kwargs: Anything that :py:func:`put` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params`` and ``json``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        dtos = save_request_from_t2s(task_to_students)
        return self.save_student_classifications(course_code, dtos,
                                                 semester, **kwargs)

    @refresh_token
    def find_student_classification(self, course_code: str,
                                    student_username: str,
                                    semester: str=None, lang: str=None,
                                    **kwargs) -> DictOrNone:
        """Find student classifications.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            student_username: The username of the student.
            semester: Semester identifier.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/courses/{course_code}'
                                f'/student-classifications'
                                f'/{student_username}',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)

    # -----------------------------------------------
    # ---------- STUDENT GROUP CONTROLLER -----------
    # -----------------------------------------------
    @refresh_token
    def get_course_groups(self, course_code: str,
                          semester: str=None, lang: str=None,
                          **kwargs) -> DictOrNone:
        """Get course groups.

        See `Classification portal API documentation
        <https://rozvoj.fit.cvut.cz/evolution-dev/
        classification/api/v1/private/documentation>`__.

        Args:
            course_code: The code of the course.
            semester: Semester identifier.
            lang: Language tag.
            **kwargs: Anything that :py:func:`get` function
                from `Requests
                <http://docs.python-requests.org/en/master/>`__
                library can take except for ``params``.

        Returns:
            On success, it returns the response body or ``None``,
            if the body is empty.

        Note:
            On failure, this method raises standard `Requests errors
            <http://docs.python-requests.org/en/master/
            _modules/requests/exceptions/>`__.

        """

        params = {'semester': semester, 'lang': lang}

        resp = self.session.get(f'{self.API_URL}/public'
                                f'/course/{course_code}'
                                f'/student-groups',
                                params=params, **kwargs)

        return get_body_or_raise_error(resp, 200)
