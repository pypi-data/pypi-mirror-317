

class PluralError(Exception):
    pass


class MissingIntentError(PluralError):
    pass


class HTTPError(PluralError):
    status_code: int
    pass


class BadRequest(HTTPError):
    status_code = 400


class Unauthorized(HTTPError):
    status_code = 401


class Forbidden(HTTPError):
    status_code = 403


class NotFound(HTTPError):
    status_code = 404
