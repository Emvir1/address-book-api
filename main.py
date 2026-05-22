from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from app.api.v1 import addresses
from app.core.config import settings
from app.core.logging import get_logger, setup_logging
from app.db.base import Base
from app.db.session import engine

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info("Starting up — environment=%s", settings.APP_ENV)
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

app.include_router(addresses.router, prefix=f"/api/{settings.API_VERSION}")

logger.info("Routes registered under /api/%s", settings.API_VERSION)
