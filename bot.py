import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from os import getenv
from dotenv import load_dotenv
from src import get_last_match_results, parse_user_config, get_allies_info_for_last_two_weeks, get_today_info_message, get_mr_incredible_sticker, sticker_ids, count_days_without_marathon, count_day_from_ex_ancient
import random

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
            fmt.text('/время - показывает, сколько времени осталось до конца рабочего дня и рабочей недели;'),
            fmt.text('/кости - подбрасывает игральные кости;'),
            fmt.text('/рама - показывает раму;'),
            fmt.text('/клоун - показывает клоуна;'),
            fmt.text('/дура - показывает дуру;'),
            fmt.text('/стата - показывает результаты твоей последней игры;'),
            fmt.text('/не_сегодня - показывает дату последней рейтинговой игры Нико;'),
            fmt.text('/куда - опрос, куда идем играть;'),
            fmt.text('/получка - стикер с получкой.'),
            fmt.text('/кенты - винрейт с кентами за последние 2 недели.'),
            fmt.text('/белка - лузстрик Рашида на белке.'),
            fmt.text('/Ибрагим - показывает Ибрагима.'),
            fmt.text('/марафон - показывает количество дней без марафона.'),
            fmt.text('/властелин - показывает, когда Михан был активным властелином.'),
            fmt.text('/пахать - отвечает на вопрос, нужно ли пахать.'),
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
        options=['Дота', 'Своя', 'На боковую', 'На завод', 'Посмотреть результаты'],
        allows_multiple_answers=True,
        is_anonymous=False
    )

    await bot.pin_chat_message(message.chat.id, msg['message_id'], disable_notification=False)


@dp.message_handler(commands='рама')
async def show_rama(message: types.Message):
    with open('media/rama.webp', 'rb') as photo:
        await message.answer_photo(photo)


@dp.message_handler(commands='клоун')
async def show_clown(message: types.Message):
    with open('media/clown.webp', 'rb') as photo:
        await message.answer_photo(photo)


@dp.message_handler(commands='дура')
async def show_dura(message: types.Message):
    dura_images = ['media/clown.webp', 'media/dura.webp']
    with open(random.choice(dura_images), 'rb') as photo:
        await message.answer_photo(photo)


@dp.message_handler(commands='домой')
async def go_home(message: types.Message):
    await message.answer_sticker(sticker_ids['go_home'])


@dp.message_handler(commands='получка')
async def salary(message: types.Message):
    await message.answer_sticker(sticker_ids['pay'])


@dp.message_handler(commands='стата')
async def last_game(message: types.Message):
    user_id = str(message.from_user.id)
    match_info_image, is_win = await get_last_match_results(user_id)

    await message.answer_photo(match_info_image)

    if is_win:
        photo_name = 'miracle'
    else:
        photo_name = 'golovach'
    with open(f'media/{photo_name}.webp', 'rb') as photo:
        await message.answer_photo(photo)

@dp.message_handler(commands='не_сегодня')
async def not_today(message: types.Message):
    match_info_image, is_win = await get_last_match_results('234173758')

    await message.answer_photo(match_info_image)

    if is_win:
        photo_name = 'miracle'
    else:
        photo_name = 'golovach'
    with open(f'media/{photo_name}.webp', 'rb') as photo:
        await message.answer_photo(photo)


@dp.message_handler(commands='кенты')
async def teammates(message: types.Message):
    user_id = str(message.from_user.id)
    statistics_image = await get_allies_info_for_last_two_weeks(user_id)

    await message.answer_photo(statistics_image)


@dp.message_handler(commands='время')
async def get_time(message: types.Message):
    user_id = str(message.from_user.id)
    await message.answer(get_today_info_message(user_id))
    await message.answer_sticker(get_mr_incredible_sticker())


@dp.message_handler(commands='белка')
async def squirrel(message: types.Message):
    with open('media/squirrel.webp', 'rb') as photo:
        await message.answer_photo(photo)
    await message.answer_sticker(sticker_ids['ronaldo'])


@dp.message_handler(commands='ибрагим')
async def ibragym(message: types.Message):
    user_id = str(message.from_user.id)

    if user_id == '207565268':
        with open('media/rock.mp4', 'rb') as gif:
            await message.answer_animation(gif)
    else:
        ibragym_images = ['media/ibragym.webp', 'media/ibragym_2.webp', 'media/ibragym_3.webp']
        with open(random.choice(ibragym_images), 'rb') as photo:
            await message.answer_photo(photo)


@dp.message_handler(commands='дуза')
async def medusa(message: types.Message):
    with open('media/medusa.webp', 'rb') as photo:
        await message.answer_photo(photo)
    await message.answer_sticker(sticker_ids['ronaldo'])


@dp.message_handler(commands='марафон')
async def marathon(message: types.Message):
    await message.answer(count_days_without_marathon())
    with open('media/marathon_promise.webp', 'rb') as photo:
        await message.answer_photo(photo)


@dp.message_handler(commands='властелин')
async def ex_ancient(message: types.Message):
    await message.answer(count_day_from_ex_ancient())


@dp.message_handler(commands='пахать')
async def work_hard(message: types.Message):
    work_urls = [
        'https://youtube.com/shorts/Ldl4BIK3Hbo?feature=share',
        'https://youtube.com/shorts/SCO2LHHY14o?feature=share'
    ]

    await message.answer(random.choice(work_urls))

if __name__ == "__main__":
    parse_user_config()
    executor.start_polling(dp, skip_updates=True)
