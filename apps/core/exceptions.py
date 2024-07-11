import logging
import traceback
from contextlib import suppress

from django.core.exceptions import (
    ObjectDoesNotExist,
)
from django.core.exceptions import (
    ValidationError as DjangoValidationError,
)
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from apps.core.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)

unique_constraint_error_messages = {
    # "db_constraint_name": "human_readable_error_message"
}

check_constraint_error_messages = {
    # "db_constraint_name": "human_readable_error_message"
}


def get_database_error_detail(exc: IntegrityError) -> tuple[str, int]:
    error_message = str(exc)

    # I usually use a postfix (e.g. "_unique_const" for constraint name to prevent any name conflicts
    for unique_constraint in unique_constraint_error_messages:
        if unique_constraint in error_message:
            return (
                unique_constraint_error_messages[unique_constraint],
                status.HTTP_409_CONFLICT,
            )

    # I usually use a postfix (e.g. "_check_const" for constraint name to prevent any name conflicts
    for check_constraint in check_constraint_error_messages:
        if check_constraint in error_message:
            return (
                check_constraint_error_messages[check_constraint],
                status.HTTP_400_BAD_REQUEST,
            )

    logger.exception({"message": error_message}, exc_info=exc)
    return "Data integrity error.", status.HTTP_503_SERVICE_UNAVAILABLE


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if not response:
        if isinstance(exc, IntegrityError):
            error_message, status_code = get_database_error_detail(exc)
            return Response({"message": error_message}, status=status_code)

        if isinstance(exc, ObjectDoesNotExist):
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        if isinstance(exc, DjangoValidationError):
            response_data = {"message": exc.messages[0]}
            with suppress(IndexError):
                if exc.messages[1:]:
                    response_data |= {"errors": exc.messages[1:]}

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    logger.exception(
        {"message": str(exc), "traceback": traceback.format_exception(exc)},
        exc_info=exc,
    )
    return response
