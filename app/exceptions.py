from fastapi import HTTPException, status


class IncorrectEmailOrPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверная почта или пароль"
        )


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек")


class TokenAbsentException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отсутствует"
        )


class BadTokenFormatException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный формат токена"
        )


class UserIsNotPresentException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="401_UNAUTHORIZED"
        )


class SlotCantBeBooking(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Слот не может быть забронирован",
        )


class ServiceCantBeAdded(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Услуги не могут быть добавлены",
        )


class InvalidDataException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Неверный формат данных или не получилось привезти к типу",
        )


class BookingCreationFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="База данных временно недоступна",
        )
