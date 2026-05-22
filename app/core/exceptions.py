from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.logging import get_logger

logger = get_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(
            "Validation error — %s %s — %s",
            request.method,
            request.url.path,
            exc.errors(),
        )
        return JSONResponse(status_code=422, content={"detail": exc.errors()})

    @app.exception_handler(SQLAlchemyError)
    async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.error(
            "Database error — %s %s — %s",
            request.method,
            request.url.path,
            str(exc),
        )
        return JSONResponse(status_code=500, content={"detail": "A database error occurred"})
