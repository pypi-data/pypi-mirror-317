from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger
import traceback

from starlette.requests import Request
from starlette.responses import JSONResponse


class ASGIErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            error_details = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
            logger.critical(
                f"ASGI Exception | Path: {request.url.path} | Method: {request.method} | Details: {error_details}"
            )
            return JSONResponse(
                {"detail": "An internal server error occurred. Please contact support."},
                status_code=500,
            )
