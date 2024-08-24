import logging
import asyncio
import asyncpg

from aiogram import Bot, Dispatcher
from src.handlers.handlers import register_handlers
from src.config import load_config
from src.middlewares.db import db_session

async def main():
    config = load_config()
    
    bot_token = config.bot_config.token

    if not bot_token:
        exit('Error: no token provided')

    bot = Bot(token=bot_token)
    pool = await asyncpg.create_pool(
            database=config.db_config.name,
            user=config.db_config.user,
            password=config.db_config.password,
            host=config.db_config.host,
            port=config.db_config.port
        )

    dp = Dispatcher()
    dp.update.middleware.register(db_session(pool))
    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    asyncio.run(main())