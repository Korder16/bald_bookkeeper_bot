import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
from src.handlers.handlers import register_handlers

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()
bot_token = getenv("BALD_BOOKKEEPER_BOT_TOKEN")

if not bot_token:
    exit('Error: no token provided')

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(content_types=['photo'])
async def photo_handler(message: types.Message):
    if message.from_user.id == 406351790:
        await message.answer(message.photo[-1].file_id)

if __name__ == "__main__":
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)
