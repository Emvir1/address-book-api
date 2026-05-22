from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.v1 import addresses
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.db.base import Base
from app.db.session import engine

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up - environment=%s", settings.APP_ENV)
    # create_all is a no-op when tables already exist, so it is safe to call
    # on every startup without risking data loss.
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready")
    yield
    logger.info("Shutting down")


app = FastAPI(
    title="Address Book API",
    description="Create, update, delete and search addresses by location.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(addresses.router, prefix=f"/api/{settings.API_VERSION}")


@app.get("/", tags=["Health"])
def health_check() -> JSONResponse:
    logger.info("Health check requested")
    return JSONResponse(content={"status": "ok", "version": app.version, "environment": settings.APP_ENV})

logger.info("Routes registered under /api/%s", settings.API_VERSION)
