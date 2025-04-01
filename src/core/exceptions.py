from fastapi import HTTPException, status


class BaseException(HTTPException):  # <-- наследуемся от HTTPException, который наследован от Exception

    # change response of exception to
    # raise HTTPException(status_code=400, detail={
    #     "status": "error",
    #     "detail": detail,
    #     "data": str(e) if str(e) else None
    # })

    status_code = 500  # <-- задаем значения по умолчанию
    detail = ""

    def __init__(self, detail: str = None):
        if detail is not None:
            self.detail = detail
        super().__init__(status_code=self.status_code, detail={
            "status": "error",
            "detail": self.detail,
            "data": None
        })


class UserAlreadyExistsWithThisEmailException(BaseException):  # # <-- наследуемся от BaseException
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists with this email"


class UserNotFoundException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid username or password"

    def __init__(self, detail: str = None):
        super().__init__(detail=detail)


class NotFoundException(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Module not found"

    def __init__(self, detail: str = None):
        super().__init__(detail=detail)


class IncorrectEmailOrPasswordException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect email or password"


class NotAuthenticatedException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Not authenticated"


class NotAuthorizedException(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Not authorized"


class NotValidCredentialsException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"


class TokenExpiredException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"


# get detail from exception object
class AlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Already exists"

    def __init__(self, detail: str = None):
        super().__init__(detail=detail)


class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(BaseAPIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


class ValidationException(BaseAPIException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class AuthenticationException(BaseAPIException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class PermissionException(BaseAPIException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )


class DatabaseException(BaseAPIException):
    def __init__(self, detail: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )
