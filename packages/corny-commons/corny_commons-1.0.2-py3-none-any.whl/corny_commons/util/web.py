"""Utility functions for all web APIs."""

# Standard library imports
import time

# Third-party imports
import requests


def send_log(*msg, force: bool = False, **kwargs):
    """Function that defines the log behaviour. By default, alias of `print`.

    Intended to be redefined with another log function with the following signature:
    `def send_log(*msg, force) -> None: ...`
    """
    if not force:
        return
    print(*msg, **kwargs)


MAX_REQUEST_COOLDOWN: int = 3  # Must wait 3s since last request


class WebException(Exception):
    """Base class for all web request-related exceptions."""


class TooManyRequestsException(WebException):
    """Raised when the user tries to make more than one request per second.

    Attributes:
        time_since_last_request -- the time since the last request, in milliseconds
        message -- explanation of the error
    """

    last_request_time: int = 0

    def __init__(
        self, current_time: int, message="You must must wait for another {cooldown}s."
    ):
        self.cooldown = (
            f"{self.last_request_time + MAX_REQUEST_COOLDOWN - current_time:.2f}"
        )
        self.message = message.format(cooldown=self.cooldown)
        super().__init__(self.message)


class InvalidResponseException(WebException):
    """Raised when the request returns with an invalid status code.

    Attributes:
        status_code -- the response status code
        message -- explanation of the error
    """

    _MESSAGE_TEMPLATE = "Invalid web response! Status code: {status_code}."

    def __init__(self, status_code: int, message: str = _MESSAGE_TEMPLATE):
        self.status_code = status_code
        self.message = message.format(status_code=status_code)
        super().__init__(self.message)


def make_request(
    url: str,
    headers: dict = None,
    params: dict = None,
    ignore_request_limit: bool = False,
) -> requests.Response:
    """Make a web request.

    Arguments:
        url -- the url of resource whose data should be requested.
        headers -- a dictionary containing the header keys and values.
        ignore_request_limit -- a boolean indicating if the 3 second limit should be ignored.

    Raises:
        web.TooManyRequestsException if there was more than one request made per 3 seconds.
        web.InvalidResponseException if the request timed out or if it responds with an error code.
    """
    current_time = time.time()
    time_passed = current_time - TooManyRequestsException.last_request_time
    if time_passed < MAX_REQUEST_COOLDOWN and not ignore_request_limit:
        raise TooManyRequestsException(int(current_time))
    TooManyRequestsException.last_request_time = current_time
    send_log(f"Fetching content from {url} ...", force=True)
    try:
        # Waits 10s for response
        response = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.exceptions.ReadTimeout as timeout_exc:
        raise InvalidResponseException(408) from timeout_exc
    if not 200 <= response.status_code < 300:
        raise InvalidResponseException(response.status_code)
    return response


def get_html(url: str, ignore_request_limit: bool) -> str:
    """Same as `make_request()`, but returns the response's decoded HTML content."""
    res = make_request(url, ignore_request_limit=ignore_request_limit)
    html = res.content.decode("UTF-8")
    return html.replace("<html><head>", "<html>\n<head>", 1)
