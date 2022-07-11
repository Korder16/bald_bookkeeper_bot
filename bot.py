import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from os import getenv
from bookkeeper import is_rashid_relaxing, get_diff_working_hours

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

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
            fmt.text('рама - показывает РАМУ'),
            sep='\n'
        ), parse_mode='HTML'
    )

@dp.message_handler(commands='кости')
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")
   
 
@dp.message_handler(commands='рама')
async def show_rama(message: types.Message):
    photo = open('media/rama.jpg', 'rb')
    await message.answer_photo(photo)


@dp.message_handler(commands='домой')
async def go_home(message: types.Message):
    await message.answer_sticker('CAACAgIAAxkBAAEFPvNizFgQ9nKuLwGp_kaDdp9DI2VpLgACERQAAqAAAehLhynfNnamXaEpBA')


@dp.message_handler(commands='время')
async def get_time(message: types.Message):
    print(message.chat)
    first_name = str(message.chat.first_name)
    username = str(message.chat.username)
    
    diff_working_hours = get_diff_working_hours(username)
    answer_message = f'{first_name}, {diff_working_hours}'
    if username != 'rash708':
        if not is_rashid_relaxing():
            answer_message += f"\nА вот Рашиду {get_diff_working_hours('rash708')}"
        else:
            answer_message += '\nА вот Рашид уже отдыхает)'
        
    await message.answer(answer_message)
    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)