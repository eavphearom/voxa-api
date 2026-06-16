import logging

from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.response import Response
from rest_framework.views import exception_handler

from app.Exceptions.application_exception import ApplicationException
from app.Exceptions.not_found_exception import NotFoundException
from app.Exceptions.validation_exception import ValidationException


logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    if isinstance(exc, (AuthenticationFailed, NotAuthenticated)):
        return Response(
            {
                "error": True,
                "status": "Unauthorized",
                "errors": [],
                "message": "Token is invalid",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            return Response(
                {
                    "error": True,
                    "status": "Unauthorized",
                    "errors": [],
                    "message": "Token is invalid",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return response

    if isinstance(exc, NotFoundException):
        return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, ValidationException):
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, ApplicationException):
        logger.exception("Application exception: %s", exc)
        return Response({"detail": str(exc)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return None
