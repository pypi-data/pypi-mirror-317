class JAuthBaseException(Exception):
    def __init__(self, message: str):
        self.message = message


class JAuthClientException(JAuthBaseException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class JAuthServerException(JAuthBaseException):
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class JAuthConnectionException(JAuthBaseException): ...


class JAuthTimeoutException(JAuthBaseException): ...


class JAuthRequestException(JAuthBaseException): ...


class JAuthAuthenticationException(JAuthBaseException): ...
