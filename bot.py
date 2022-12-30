import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from os import getenv
from dotenv import load_dotenv
from src import get_working_hours_info, get_last_match_results


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


@dp.message_handler(commands='help')
async def help(message: types.Message):
    await message.answer(
        fmt.text(
            fmt.text('Список доступных комманд: '),
            fmt.text('время - показывает, сколько времени осталось до конца рабочего дня;'),
            fmt.text('кости - подбрасывает игральные кости;'),
            fmt.text('рама - показывает раму;'),
            fmt.text('клоун - показывает клоуна;'),
            fmt.text('стата - показывает результаты твоей последней игры;'),
            fmt.text('не_сегодня - показывает дату последней рейтинговой игры Нико;'),
            fmt.text('куда - опрос, куда идем играть;'),
            fmt.text('получка - стикер с получкой.'),
            sep='\n'
        ), parse_mode='HTML'
    )


@dp.message_handler(commands='кости')
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message_handler(commands='куда')
async def sigame_poll(message: types.Message):
    msg = await message.answer_poll(
        question='Куда идем?',
        options=['Дота', 'Своя', 'На боковую'],
        allows_multiple_answers=True,
        is_anonymous=False
    )

    await bot.pin_chat_message(message.chat.id, msg['message_id'], disable_notification=False)


@dp.message_handler(commands='рама')
async def show_rama(message: types.Message):
    photo = open('media/rama.jpg', 'rb')
    await message.answer_photo(photo)


@dp.message_handler(commands=['клоун', 'дура'])
async def show_clown(message: types.Message):
    photo = open('media/clown.jpg', 'rb')
    await message.answer_photo(photo)


@dp.message_handler(commands='домой')
async def go_home(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEFPvNizFgQ9nKuLwGp_kaDdp9DI2VpLgACERQAAqAAAehLhynfNnamXaEpBA')


@dp.message_handler(commands='получка')
async def salary(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEBLThizZnIHTLfN24LodNlBXYilqcoNQAC-w8AArGreUvmmZ8F9DW_NSkE')


@dp.message_handler(commands='стата')
async def last_game(message: types.Message):
    username = str(message.from_user.username)
    match_info_image_bytes = await get_last_match_results(username)

    await message.answer_photo(match_info_image_bytes)


@dp.message_handler(commands='не_сегодня')
async def not_today(message: types.Message):
    match_info_image_bytes = await get_last_match_results('NikoGasanov')

    await message.answer_photo(match_info_image_bytes)


@dp.message_handler(commands='время')
async def get_time(message: types.Message):
    print(message.from_user)
    first_name = str(message.from_user.first_name)
    username = str(message.from_user.username)

    answer_message = f'{first_name}, {get_working_hours_info(username)}'
    await message.answer(answer_message)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
