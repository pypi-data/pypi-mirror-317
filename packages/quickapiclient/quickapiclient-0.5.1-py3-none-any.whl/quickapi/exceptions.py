from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from quickapi.http_clients.types import BaseHttpClientResponse
    from quickapi.serializers.types import DictSerializableT


class QuickApiException(Exception):
    """A QuickApi exception has occurred."""


class ClientSetupError(QuickApiException):
    """An error setting up the `BaseClient` subclass."""

    def __init__(self, attribute: str):
        message = (
            f"Client setup error. Missing or invalid required attribute `{attribute}`."
        )
        super().__init__(message)


class ApiSetupError(QuickApiException):
    """An error setting up the `BaseApi` subclass."""

    def __init__(self, attribute: str):
        message = (
            f"Api setup error. Missing or invalid required attribute `{attribute}`."
        )
        super().__init__(message)


class HTTPError(QuickApiException):
    """The response received a non `200` response status code."""

    status_code: int
    body: "DictSerializableT | str"
    handled: bool = False

    def __init__(
        self,
        client_response: "BaseHttpClientResponse",
        status_code: int,
        body: "DictSerializableT | str",
        handled: bool = False,
    ):
        message = f"HTTP request received a non `HTTP 200 (OK)` response. The response status code was `{status_code}`."
        self.status_code = status_code
        self.body = body
        self.handled = handled
        super().__init__(message)


class DictSerializationError(QuickApiException):
    """Dict serialization failed."""

    expected_type = ""

    def __init__(self, expected_type: str):
        self.expected_type = expected_type
        super().__init__(self.__doc__)


class DictDeserializationError(QuickApiException):
    """Dict deserialization failed."""

    expected_type = ""

    def __init__(self, expected_type: str):
        self.expected_type = expected_type
        super().__init__(self.__doc__)


class ResponseSerializationError(QuickApiException):
    """The response received was not serializable to the configured `response_body` type."""

    def __init__(self, expected_type: str):
        message = f"HTTP response body did not match expected type `{expected_type}`."
        super().__init__(message)


class RequestSerializationError(QuickApiException):
    """The request was not serializable to the configured type."""

    def __init__(self, expected_type: str):
        message = (
            f"HTTP request params/body did not match expected type `{expected_type}`."
        )
        super().__init__(message)


class MissingDependencyError(QuickApiException):
    """Trying to use an optional dependency without installing it first."""

    def __init__(self, dependency: str):
        message = (
            f"Using an optional dependecy without installing it first `{dependency}`."
            f"Please install the dependency using `pip install quickapiclient[{dependency}]`."
        )
        super().__init__(message)
