from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger


class ExceptionHandlers:
    @staticmethod
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """
        Handle HTTP exceptions.
        """
        logger.error(f"HTTP Exception: {exc.detail} | Path: {request.url.path}")
        return JSONResponse(
            {"detail": exc.detail},
            status_code=exc.status_code,
        )

    @staticmethod
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        Handle validation errors.
        """
        logger.warning(f"Validation error: {exc.errors()} | Path: {request.url.path}")
        return JSONResponse(
            {"detail": exc.errors()},
            status_code=422,
        )
