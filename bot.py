import logging
from aiogram import Bot, Dispatcher, executor
from src.handlers.handlers import register_handlers
from src.config import load_config

if __name__ == "__main__":
    config = load_config()
    bot_token = config.bot_config.token

    if not bot_token:
        exit('Error: no token provided')

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bot = Bot(token=bot_token)
    dp = Dispatcher(bot)

    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
