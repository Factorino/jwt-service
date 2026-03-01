from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from app.main.configs.config import Config
from app.main.configs.toml_loader import load_config
from app.main.di.container import create_container
from app.presentation.api.error_handler import app_error_handler
from app.presentation.api.routers.auth import router as auth_router
from app.presentation.api.routers.root import router as root_router
from app.presentation.api.routers.user import router as user_router


if TYPE_CHECKING:
    from dishka import AsyncContainer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


def create_app(config: Config) -> FastAPI:
    app = FastAPI(
        title="Auth API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.api.cors.allow_origins,
        allow_credentials=config.api.cors.allow_credentials,
        allow_methods=config.api.cors.allow_methods,
        allow_headers=config.api.cors.allow_headers,
        max_age=config.api.cors.max_age,
    )

    container: AsyncContainer = create_container(config)
    setup_dishka(container, app)

    app.include_router(root_router)
    app.include_router(auth_router)
    app.include_router(user_router)
    app.add_exception_handler(Exception, app_error_handler)

    return app


def main() -> None:
    config: Config = load_config(Config)
    app: FastAPI = create_app(config)

    uvicorn.run(
        app,
        host=config.api.host,
        port=config.api.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
