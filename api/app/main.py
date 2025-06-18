import asyncio
import logging
from contextlib import asynccontextmanager

from app.api import api_router
from app.config import settings
from app.enums import Environment
from app.jobs.price_updater import update_prices_periodically
from app.models import *  # noqa
from app.rate_limiter import limiter
from asyncpg.exceptions import ConnectionFailureError
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

log = logging.getLogger(__name__)


description = """
APIs for Runescape.
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(update_prices_periodically())

    yield


# TODO Configure by environment
app = FastAPI(
    title="Runescape", description=description, root_path="/api/v1", lifespan=lifespan
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=settings.CORS_HEADERS,
    allow_credentials=True,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
)

if settings.ENVIRONMENT == Environment.PRODUCTION:

    @app.exception_handler(ConnectionFailureError)
    async def connection_failure_exception_handler(
        request: Request, exc: ConnectionFailureError
    ):
        logging.error(f"Connection failure: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content="Service is unavailable, please try again later",
        )

    @app.exception_handler(ValueError)
    async def value_error_exception_handler(request: Request, exc: ValueError):
        logging.error(f"Value error: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def catchall_exception_handler(request: Request, exc: Exception):
        logging.error(f"Unhandled exception: {str(exc)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


app.include_router(api_router)


@app.get("/")
async def root(request: Request):
    return {"message": "Welcome to Runescape"}
