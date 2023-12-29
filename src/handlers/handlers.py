from aiogram import Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
import aiogram.utils.markdown as fmt

from ..sql_client import bald_bookeeper_bot_db_client
from ..stickers import sticker_ids
from ..bookkeeper import count_day_from_ex_ancient, count_days_without_marathon
from ..dota.opendota_api_client import get_last_match_results, get_allies_info_for_last_two_weeks
from ..image_generator_api_client import image_api_generator_client
from ..bookkeeper import get_today_info_message, get_mr_incredible_sticker

from random import choice

router = Router()


async def get_last_match_result_image_id(is_win: bool):
    db_client = bald_bookeeper_bot_db_client()

    if is_win:
        photo_name = await db_client.get_miracle_file_id()
    else:
        photo_name = await db_client.get_golovach_file_id()

    return photo_name


async def last_game_impl(message: Message, user_id: int):
    last_match_results, is_win = await get_last_match_results(str(user_id))

    db_client = bald_bookeeper_bot_db_client()
    dota_account_id = await db_client.get_dota_id_by_tg_id(user_id)
    db_last_match_id = await db_client.get_last_match_id(dota_account_id)

    is_match_image_file_id_exists = await db_client.is_match_image_file_id_exists(db_last_match_id)
    if is_match_image_file_id_exists:
        match_image_file_id = await db_client.get_match_image_file_id(db_last_match_id)
        await message.answer_photo(photo=match_image_file_id)
    else:
        client = image_api_generator_client()
        response_image = await client.get_last_game_statistics_image(last_match_results)
        response_buffered_file = BufferedInputFile(response_image, filename='last_game.webp')
        sent_photo = await message.answer_photo(response_buffered_file)

        await db_client.insert_match_image_file_id(db_last_match_id, sent_photo.photo[0].file_id)

    await message.answer_photo(photo=await get_last_match_result_image_id(is_win))


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
            fmt.text('/белка - лузстрик Рашида на белке.'),
            fmt.text('/позор - игра Ислама на аксе 0 24.'),
            fmt.text('/лега - 82 урона с дуэлей за 50 минут от Дениса.'),
            fmt.text('/Ибрагим - показывает Ибрагима.'),
            fmt.text('/марафон - показывает количество дней без марафона.'),
            fmt.text('/властелин - показывает, когда Михан был активным властелином.'),
            fmt.text('/пахать - отвечает на вопрос, нужно ли пахать.'),
            fmt.text('/пацаны - показывает Рашида + пацана.'),
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
async def teammates(message: Message):
    user_id = str(message.from_user.id)
    allies_info = await get_allies_info_for_last_two_weeks(user_id)

    client = image_api_generator_client()
    response_image = await client.get_teammates_statistics_image(user_id, allies_info)
    response_buffered_file = BufferedInputFile(response_image, filename='teammates.webp')
    await message.answer_photo(response_buffered_file)


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


@router.message(Command("пацаны"))
async def guys(message: Message):
    await message.answer_photo(photo=await bald_bookeeper_bot_db_client().get_guys_file_id())


def register_handlers(dp: Dispatcher):
    dp.include_router(router)
