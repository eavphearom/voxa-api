from app.Exceptions.application_exception import ApplicationException


class ValidationException(ApplicationException):
    default_message = "Validation failed"
