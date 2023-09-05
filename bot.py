import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from os import getenv
from dotenv import load_dotenv
from src import get_last_match_results, get_allies_info_for_last_two_weeks, get_today_info_message, get_mr_incredible_sticker, sticker_ids, count_days_without_marathon, count_day_from_ex_ancient
import random
from src import image_api_generator_client
from src.sql_client import bald_bookeeper_bot_db_client

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
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_rama_file_id())


@dp.message_handler(commands='клоун')
async def show_clown(message: types.Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_clown_file_id())


@dp.message_handler(commands='дура')
async def show_dura(message: types.Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_random_dura_file_id())


@dp.message_handler(commands='домой')
async def go_home(message: types.Message):
    await message.answer_sticker(sticker_ids['go_home'])


@dp.message_handler(commands='получка')
async def salary(message: types.Message):
    await message.answer_sticker(sticker_ids['pay'])


async def get_last_match_result_image_id(is_win: bool):
    db_client = bald_bookeeper_bot_db_client()

    if is_win:
        photo_name = await db_client.get_miracle_file_id()
    else:
        photo_name = await db_client.get_golovach_file_id()

    return photo_name


async def last_game_impl(message: types.Message, user_id: int):
    last_match_results, is_win = await get_last_match_results(str(user_id))

    db_client = bald_bookeeper_bot_db_client()
    dota_account_id = await db_client.get_dota_id_by_tg_id(user_id)
    db_last_match_id = await db_client.get_last_match_id(dota_account_id)

    if await db_client.is_match_image_file_id_exists(db_last_match_id):
        match_image_file_id = await db_client.get_match_image_file_id(db_last_match_id)
        await message.answer_photo(photo=match_image_file_id)
    else:
        client = image_api_generator_client()
        response_image = await client.get_last_game_statistics_image(last_match_results)
        sent_photo = await message.answer_photo(response_image)

        await db_client.insert_match_image_file_id(db_last_match_id, sent_photo.photo[0].file_id)

    await message.answer_photo(photo=await get_last_match_result_image_id(is_win))


@dp.message_handler(commands='стата')
async def last_game(message: types.Message):
    user_id = str(message.from_user.id)
    await last_game_impl(message, user_id)


@dp.message_handler(commands='не_сегодня')
async def not_today(message: types.Message):
    await last_game_impl(message, 234173758)


@dp.message_handler(commands='кенты')
async def teammates(message: types.Message):
    user_id = str(message.from_user.id)
    allies_info = await get_allies_info_for_last_two_weeks(user_id)

    client = image_api_generator_client()
    response_image = await client.get_teammates_statistics_image(user_id, allies_info)
    await message.answer_photo(response_image)


@dp.message_handler(commands='время')
async def get_time(message: types.Message):
    user_id = message.from_user.id
    await message.answer(await get_today_info_message(user_id))
    await message.answer_sticker(get_mr_incredible_sticker())


@dp.message_handler(commands='белка')
async def squirrel(message: types.Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_squirrel_file_id())
    await message.answer_sticker(sticker_ids['ronaldo'])


@dp.message_handler(commands='ибрагим')
async def ibragym(message: types.Message):
    user_id = str(message.from_user.id)
    db_client = bald_bookeeper_bot_db_client()
    if user_id == '207565268':
        await message.answer_animation(animation=await db_client.get_squirrel_file_id())
    else:
        await message.answer_photo(photo=await db_client.get_random_ibragym_file_id())


@dp.message_handler(commands='дуза')
async def medusa(message: types.Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_medusa_file_id())
    await message.answer_sticker(sticker_ids['ronaldo'])


@dp.message_handler(commands='марафон')
async def marathon(message: types.Message):
    await message.answer(count_days_without_marathon())
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_marathon_file_id())


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
    executor.start_polling(dp, skip_updates=True)
