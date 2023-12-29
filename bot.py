import logging
from aiogram import Bot, Dispatcher, executor
from os import getenv
from dotenv import load_dotenv
from src.handlers.handlers import register_handlers

if __name__ == "__main__":

    load_dotenv()
    bot_token = getenv("BALD_BOOKKEEPER_BOT_TOKEN")

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
