from app.Exceptions.application_exception import ApplicationException


class NotFoundException(ApplicationException):
    default_message = "Resource not found"
