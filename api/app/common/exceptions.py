from fastapi import HTTPException, WebSocketException, status


class NotAuthorized(HTTPException):
    def __init__(self, error_msg: str = None):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = [{"msg": error_msg or "Not authorized to perform this action."}]

        super().__init__(status_code=status_code, detail=detail)


class Forbidden(HTTPException):
    def __init__(self, error_msg: str = None):
        status_code = status.HTTP_403_FORBIDDEN
        detail = [{"msg": error_msg or "Forbidden."}]

        super().__init__(status_code=status_code, detail=detail)


class NotFound(HTTPException):
    def __init__(self, error_msg: str = None):
        status_code = status.HTTP_404_NOT_FOUND
        detail = [{"msg": error_msg or "Resource not found."}]

        super().__init__(status_code=status_code, detail=detail)


class UnprocessableEntity(HTTPException):
    def __init__(self, error_msg: str = None):
        status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = [{"msg": error_msg or "Request cannot be processed."}]

        super().__init__(status_code=status_code, detail=detail)


class Conflict(HTTPException):
    def __init__(self, error_msg: str = None):
        status_code = status.HTTP_409_CONFLICT
        detail = [{"msg": error_msg or "Conflict."}]

        super().__init__(status_code=status_code, detail=detail)


# Websocket exceptions
class WSUnsupportedData(WebSocketException):
    """Exception for websocket"""

    def __init__(self):
        super().__init__(code=status.WS_1003_UNSUPPORTED_DATA)
