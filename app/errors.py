from collections.abc import Mapping

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from contracts.common import ErrorResponse


class RelayApiError(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "relay_error"

    def __init__(self, message: str, *, context: Mapping[str, str] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.context = dict(context or {})


class ResourceNotFoundError(RelayApiError):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "resource_not_found"

    def __init__(self, resource_type: str, resource_id: str) -> None:
        super().__init__(
            f"{resource_type} '{resource_id}' was not found.",
            context={"resource_type": resource_type, "resource_id": resource_id},
        )


class InvalidComparisonRequestError(RelayApiError):
    status_code = status.HTTP_400_BAD_REQUEST
    error_code = "invalid_comparison_request"


def _error_response(error: RelayApiError) -> ErrorResponse:
    return ErrorResponse(
        error=error.error_code,
        message=error.message,
        context=error.context,
    )


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(RelayApiError)
    async def handle_relay_error(_: Request, exc: RelayApiError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_response(exc).model_dump(),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        payload = ErrorResponse(
            error="request_validation_error",
            message="The request payload or query parameters were invalid.",
            context={"issues": str(exc.errors())},
        )
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload.model_dump())
