


class Exceptions:
    class IncorrectIdType(Exception):
        """Неверный идентификатор объекта."""
        def __init__(self, message="Неверный идентификатор объекта: {incorrectId}", incorrectId: str = ''):
            super().__init__(message.format(incorrectId=incorrectId))
    
    class UnexpectedError(Exception):
        """Неожиданная ошибка"""
        def __init__(self, message="Неожиданная ошибка"):
            super().__init__(message)
    