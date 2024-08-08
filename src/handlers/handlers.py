from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, URLInputFile
import aiogram.utils.markdown as fmt

from ..sql_client import bald_bookeeper_bot_db_client
from ..stickers import sticker_ids
from ..bookkeeper import count_day_from_ex_ancient, count_days_without_marathon
from ..image_generator_api_client import image_api_generator_client
from ..bookkeeper import get_today_info_message, get_mr_incredible_sticker
from ..config import load_config

from random import choice

router = Router()
config = load_config()

async def get_last_match_result_image_id(is_win: bool):
    db_client = bald_bookeeper_bot_db_client()

    if is_win:
        photo_name = await db_client.get_miracle_file_id()
    else:
        photo_name = await db_client.get_golovach_file_id()

    return photo_name


async def last_game_impl(message: Message, user_id: int):
    db_client = bald_bookeeper_bot_db_client()
    dota_account_id = await db_client.get_dota_id_by_tg_id(user_id)

    client = image_api_generator_client()
    response = await client.get_last_game_statistics_image(dota_account_id)
    
    # TODO: add cache
    image_url = f"http://{config.image_generator_config.host}:{config.image_generator_config.port}/images/{response['image_path']}"
    image = URLInputFile(image_url)
    await message.answer_photo(photo=image)
    await message.answer_photo(photo=await get_last_match_result_image_id(response['is_win']))


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(
        fmt.text(
            fmt.text('Список доступных комманд: '),
            fmt.text('/время - показывает, сколько времени осталось до конца рабочего дня и рабочей недели;'),
            fmt.text('/рама - показывает раму;'),
            fmt.text('/клоун - показывает клоуна;'),
            fmt.text('/дура - показывает дуру;'),
            fmt.text('/стата - показывает результаты твоей последней игры;'),
            fmt.text('/не_сегодня - показывает дату последней рейтинговой игры Нико;'),
            fmt.text('/куда - опрос, куда идем играть;'),
            fmt.text('/получка - стикер с получкой.'),
            fmt.text('/кенты - винрейт с кентами за последние 2 недели.'),
            fmt.text('/кенты_за_год - винрейт с кентами за последние 365 дней.'),
            fmt.text('/белка - лузстрик Рашида на белке.'),
            fmt.text('/позор - игра Ислама на аксе 0 24.'),
            fmt.text('/лега - 82 урона с дуэлей за 50 минут от Дениса.'),
            fmt.text('/Ибрагим - показывает Ибрагима.'),
            fmt.text('/марафон - показывает количество дней без марафона.'),
            fmt.text('/властелин - показывает, когда Михан был активным властелином.'),
            fmt.text('/пахать - отвечает на вопрос, нужно ли пахать.'),
            fmt.text('/пацаны - показывает Рашида + пацана.'),
            fmt.text('/статистика_за_год - показывает статистику в доте за год.'),
            fmt.text('/стрелочники - показывает стрелочников в доте.'),
            sep='\n'
        ), parse_mode='HTML'
    )


@router.message(Command("белка"))
async def squirrel(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_squirrel_file_id())
    await message.answer_sticker(sticker_ids['ronaldo'])


@router.message(Command("ибрагим"))
async def ibragym(message: Message):
    user_id = str(message.from_user.id)
    db_client = bald_bookeeper_bot_db_client()
    if user_id == '207565268':
        await message.answer_animation(animation=await db_client.get_rock_file_id())
    else:
        await message.answer_photo(photo=await db_client.get_random_ibragym_file_id())


@router.message(Command("дуза"))
async def medusa(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_medusa_file_id())
    await message.answer_sticker(sticker_ids['ronaldo'])


@router.message(Command("марафон"))
async def marathon(message: Message):
    await message.answer(count_days_without_marathon())
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_marathon_file_id())


@router.message(Command("властелин"))
async def ex_ancient(message: Message):
    await message.answer(count_day_from_ex_ancient())


@router.message(Command("лега"))
async def legion_commander(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_legion_commander_file_id())
    await message.answer_sticker(sticker_ids['ronaldo'])


@router.message(Command("позор"))
async def shame(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_shame_file_id())
    await message.answer_sticker(sticker_ids['ronaldo'])


@router.message(Command("куда"))
async def choose_activity(message: Message):
    msg = await message.answer_poll(
        question='Куда идем?',
        options=['Дота', 'Своя', 'На боковую', 'На завод', 'Посмотреть результаты'],
        allows_multiple_answers=True,
        is_anonymous=False
    )

    await msg.pin()


@router.message(Command("рама"))
async def show_rama(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_rama_file_id())


@router.message(Command("клоун"))
async def show_clown(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_clown_file_id())


@router.message(Command("дура"))
async def show_dura(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_random_dura_file_id())


@router.message(Command("домой"))
async def go_home(message: Message):
    await message.answer_sticker(sticker_ids['go_home'])


@router.message(Command("получка"))
async def salary(message: Message):
    await message.answer_sticker(sticker_ids['pay'])


@router.message(Command("стата"))
async def last_game(message: Message):
    user_id = str(message.from_user.id)
    await last_game_impl(message, user_id)


@router.message(Command("не_сегодня"))
async def not_today(message: Message):
    await last_game_impl(message, 234173758)


@router.message(Command("кенты"))
async def teammates_last_two_weeks(message: Message):
    user_id = str(message.from_user.id)

    db_client = bald_bookeeper_bot_db_client()
    dota_account_id = await db_client.get_dota_id_by_tg_id(user_id)

    client = image_api_generator_client()
    response = await client.get_teammates_statistics_image(dota_account_id)

    image_url = f"http://{config.image_generator_config.host}:{config.image_generator_config.port}/images/{response['image_path']}"
    image = URLInputFile(image_url)
    await message.answer_photo(photo=image)


@router.message(Command("кенты_за_год"))
async def teammates_last_year(message: Message):
    user_id = str(message.from_user.id)
    allies_info = await get_allies_info_for_last_year(user_id)

    client = image_api_generator_client()
    response_image = await client.get_teammates_statistics_image(user_id, allies_info)
    response_buffered_file = BufferedInputFile(response_image, filename='teammates.webp')
    await message.answer_photo(response_buffered_file)

@router.message(Command("статистика_за_год"))
async def player_totals_last_year(message: Message):
    user_id = str(message.from_user.id)

    player_totals_info = await get_player_totals_for_last_year(user_id)

    await message.answer(player_totals_info, parse_mode='html')


@router.message(Command("время"))
async def get_time(message: Message):
    user_id = message.from_user.id
    await message.answer(await get_today_info_message(user_id))
    await message.answer_sticker(get_mr_incredible_sticker())


@router.message(Command("пахать"))
async def work_hard(message: Message):
    work_urls = [
        'https://youtube.com/shorts/Ldl4BIK3Hbo?feature=share',
        'https://youtube.com/shorts/SCO2LHHY14o?feature=share'
    ]

    await message.answer(choice(work_urls))

# @router.message()
# async def photo_handler(message: Message):
#     if message.from_user.id == 406351790:
#         await message.answer(message.photo[-1].file_id)

@router.message(Command("стрелочники"))
async def switchmen(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_switchmen_file_id())

@router.message(Command("пацаны"))
async def guys(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_guys_file_id())


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
