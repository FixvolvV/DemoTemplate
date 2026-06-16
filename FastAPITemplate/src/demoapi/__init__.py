from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from demoapi.core.settings import settings
from demoapi.core.httpx import httpx_client_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # startup

    await httpx_client_manager.start()

    yield
    # shutdown

    await httpx_client_manager.stop()


app = FastAPI(
    lifespan=lifespan,
    docs_url=None if settings.run.mode == "production" else "/docs",  # disables docs
    redoc_url=None if settings.run.mode == "production" else "/redoc",  # disables redoc
    openapi_url=(
        None if settings.run.mode == "production" else "/openapi.json"
    ),  # disables openapi.json suggested by tobias comment.
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.httpcors.urls,  # pyright:ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
