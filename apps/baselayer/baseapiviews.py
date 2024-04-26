"""All views will extend this BaseAPIView View."""

import logging

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import is_server_error
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.views import APIView, exception_handler
from rest_framework.viewsets import ModelViewSet

logger = logging.getLogger(settings.LOGGER_NAME_PREFIX + __name__)


class ResponseBuilder:
    """Builds response body."""

    @staticmethod
    def build(msg_code, data=None, message="", pagination=None, errors_details=None):
        """Builds standard response body."""
        return {
            "msg_code": msg_code,
            "data": data if data is not None else {},
            "pagination": pagination if pagination is not None else {},
            "errors_details": errors_details if errors_details is not None else [],
            "message": message,
        }


class ResponseHandler:
    """Handles response generation."""

    @staticmethod
    def generate(status_code, msg_code, data=None, message="", pagination=None, errors_details=None):
        """Generates response."""
        response_data = ResponseBuilder.build(msg_code, data, message, pagination, errors_details)
        return Response(data=response_data, status=status_code)


class BaseAPIView(ModelViewSet):
    """Base class for API views."""

    def send_response(self, status_code, message="", data=None, pagination=None, errors_details=None):
        """Compose response."""
        return ResponseHandler.generate(status_code, data, message, pagination, errors_details)

    def send_success_response(self, message, data=None, pagination=None, errors_details=None):
        """Compose success response."""
        return self.send_response(status.HTTP_200_OK, message, data, pagination, errors_details)

    def send_created_response(self, message, data=None, pagination=None, errors_details=None):
        """Compose response for new object creation."""
        return self.send_response(status.HTTP_201_CREATED, message, data, pagination, errors_details)

    def send_bad_request_response(self, message=None, errors_details=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Compose response for bad request."""
        return self.send_response(status_code=status_code, message=message,
                                  errors_details=errors_details)

    def send_not_found_response(self, message="Not found.", errors_details=None):
        """Compose response for not found request."""
        return self.send_response(status.HTTP_404_NOT_FOUND, message, errors_details=errors_details)

    def send_internal_server_error_response(self, message="Internal server error.", errors_details=None):
        """Compose response for internal server error response."""
        return self.send_response(status.HTTP_500_INTERNAL_SERVER_ERROR, message, errors_details=errors_details)


def custom_exception_handler(exc, context):
    """Call REST framework's default exception handler to set a standard error response on error."""
    logger.info("inside of custom exception handler.")

    response = exception_handler(exc, context)
    logger.info(f" context: {context}")
    logger.error(f" exception: {exc}")
    logger.error(f" response: {response}")

    # The exception handler function should either return a Response object,or None
    # If the handler returns None then the exception will be re-raised and
    # Django will return a standard HTTP 500 'server error' response.
    # so override the response None and return standard response with HTTP_400_BAD_REQUEST
    if response is None:
        return Response(
            data={
                "success": False,
                "data": {},
                "message": "Something went wrong during process.Try again later.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response(
        data={
            "success": False,
            "data": {},
            "message": response.data["detail"],
        },
        status=response.status_code,
    )


def get_first_error_message_from_serializer_errors(
        serialized_errors, default_message=""
):
    this_field_is_required = "This field is required."
    if not serialized_errors:
        logger.error(default_message)
        return default_message
    try:
        logger.error(serialized_errors)

        serialized_error_dict = serialized_errors

        # ReturnList of serialized_errors when many=True on serializer
        if isinstance(serialized_errors, ReturnList):
            serialized_error_dict = serialized_errors[0]
        elif isinstance(serialized_errors, ValidationError):
            serialized_error_dict = serialized_errors.detail

        serialized_errors_keys = list(serialized_error_dict.keys())
        # getting first error message from serializer errors
        error_message = serialized_error_dict[serialized_errors_keys[0]][0]
        if error_message == this_field_is_required:
            error_message = error_message.replace("This", serialized_errors_keys[0])
        return error_message
    except Exception as e:
        logger.error(f"Error parsing serializer errors:{e}")
        return default_message
