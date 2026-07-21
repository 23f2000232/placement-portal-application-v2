import logging
from datetime import datetime, timezone
from http import HTTPStatus

from flask import Flask, jsonify, request
from pydantic import ValidationError

from app.enums import ErrorCode
from app.exceptions.app_exception import AppException
from app.schemas.response.api_error_response import ApiErrorResponse

logger = logging.getLogger(__name__)


def _build_error_response(
    status: HTTPStatus,
    error: ErrorCode,
    message: str,
):
    response = ApiErrorResponse(
        timestamp=datetime.now(timezone.utc),
        status=status,
        error=error,
        message=message,
        path=request.path,
    )

    return jsonify(response.model_dump(mode="json")), status.value


def register_exception_handlers(app: Flask) -> None:

    @app.errorhandler(AppException)
    def handle_app_exception(exception: AppException) -> tuple:
        return _build_error_response(
            status=exception.status_code,
            error=exception.error_code,
            message=exception.message,
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(exception: ValidationError) -> tuple:
        logger.warning("Validation failed: %s", exception)

        return _build_error_response(
            message="Validation failed",
            status=HTTPStatus.BAD_REQUEST,
            error=ErrorCode.VALIDATION_ERROR,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_exception(exception: Exception) -> tuple:
        logger.exception("Unhandled exception")

        return _build_error_response(
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
            error=ErrorCode.INTERNAL_SERVER_ERROR,
            message="An unexpected error occurred.",
        )