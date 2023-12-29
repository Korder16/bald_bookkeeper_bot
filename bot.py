import logging
import asyncio

from aiogram import Bot, Dispatcher
from src.handlers.handlers import register_handlers
from src.config import load_config

async def main():
    config = load_config()
    bot_token = config.bot_config.token

    if not bot_token:
        exit('Error: no token provided')

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    register_handlers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    asyncio.run(main())