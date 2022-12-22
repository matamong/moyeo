import asyncpg
from fastapi import FastAPI

from app.core.config import get_app_settings

APP_SETTINGS = get_app_settings()


async def connect_to_db(app: FastAPI, settings: APP_SETTINGS) -> None:
    app.state.pool = await asyncpg.create_pool(
        str(settings.database_url),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )
    print("Connection established") # Till logging


async def close_db_connection(app: FastAPI) -> None:
    await app.state.pool.close()
    print("Connection Closed")  # Till logging