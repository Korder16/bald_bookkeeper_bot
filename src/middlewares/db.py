from typing import Callable, Awaitable, Coroutine, Dict, Any
import asyncpg
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class db_session(BaseMiddleware):
    def __init__(self, connector: asyncpg.pool.Pool) -> None:
        super().__init__()
        self.connector = connector

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Coroutine[Any, Any, Any]:
        async with self.connector.acquire() as connection:
            data["db_connection"] = connection
            return await handler(event, data)
