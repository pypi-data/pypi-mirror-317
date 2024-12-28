"""Exceptions"""


class SpcException(Exception):
    """Base error for SPC."""


class RequestError(SpcException):
    """Unable to fulfill request.

    Raised when device cannot be reached.
    """


class ResponseError(SpcException):
    """Invalid response."""


class Unauthorized(SpcException):
    """Username is not authorized."""


class Forbidden(SpcException):
    """Endpoint is not accessible due to low permissions."""


class LoginRequired(SpcException):
    """User is logged out."""


class MethodNotAllowed(SpcException):
    """Invalid request."""


class PathNotFound(SpcException):
    """Path not found."""


ERRORS = {
    401: Unauthorized,
    403: Forbidden,
    404: PathNotFound,
    405: MethodNotAllowed,
}


def raise_error(error: int) -> None:
    """Raise error."""
    cls = ERRORS.get(error, SpcException)
    raise cls(error)
