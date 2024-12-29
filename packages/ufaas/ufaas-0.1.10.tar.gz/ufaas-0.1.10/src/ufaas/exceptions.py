error_messages = {}


class UFaaSException(Exception):
    def __init__(self, status_code: int, error: str, message: str = None):
        self.status_code = status_code
        self.error = error
        self.message = message
        if message is None:
            self.message = error_messages[error]
        super().__init__(message)


class InsufficientFunds(UFaaSException):
    def __init__(self, message: str = None):
        super().__init__(status_code=402, error="insufficient_funds", message=message)


class InvalidRequest(UFaaSException):
    def __init__(self, message: str = None):
        super().__init__(status_code=400, error="invalid_request", message=message)


class Unauthorized(UFaaSException):
    def __init__(self, message: str = None):
        super().__init__(status_code=401, error="unauthorized", message=message)


class Forbidden(UFaaSException):
    def __init__(self, message: str = None):
        super().__init__(status_code=403, error="forbidden", message=message)


class NotFound(UFaaSException):
    def __init__(self, message: str = None):
        super().__init__(status_code=404, error="not_found", message=message)
