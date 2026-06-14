from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from app.Exceptions.application_exception import ApplicationException
from app.Exceptions.not_found_exception import NotFoundException
from app.Exceptions.validation_exception import ValidationException


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        return response

    if isinstance(exc, NotFoundException):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, ValidationException):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, ApplicationException):
        return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return None
