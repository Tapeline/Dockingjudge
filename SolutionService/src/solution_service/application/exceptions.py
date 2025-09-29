from http.client import HTTPException


class APIException(HTTPException):
    code: str = "ERROR"
    status: int = 500
    detail: str = "Error occurred"

    def __init__(
            self,
            *,
            status_code: int | None = None,
            code: str | None = None,
            detail: str | None = None,
            **kwargs
    ):
        super().__init__()
        self.status = status_code or APIException.status
        self.code = code or APIException.code
        self.detail = detail or APIException.detail
        self.extras = kwargs


class NotFoundException(APIException):
    status = 404
    code = "OBJECT_NOT_FOUND"
    detail = "Requested object cannot be found"


class ForbiddenException(APIException):
    status = 403
    code = "NOT_ENOUGH_PERMISSIONS"
    detail = "You cannot access requested resource"
