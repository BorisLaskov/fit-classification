class SavedTokenError(Exception):
    """Error related to manipulations with the saved token.

    Raised when the file with token cannot be read
    or when it lacks some essential parts
    (like "access_token" and/or "refresh_token" fields).

    """
    pass


class AuthError(Exception):
    """Error related to authorization process.

    Raised when, for example, the "code" field
    is missing from the GET callback during login.

    """
    pass


class MissingParameterError(Exception):
    """Error related to proxy.

    Raised when some compulsory parameter is missing
    from both its attribute and argument set
    of the method invocation.

    """
    pass
