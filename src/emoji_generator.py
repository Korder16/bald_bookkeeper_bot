import emoji

emoji_numbers = {
    0: ':zero:',
    1: ':one:',
    2: ':two:',
    3: ':three:',
    4: ':four:',
    5: ':five:',
    6: ':six:',
    7: ':seven:',
    8: ':eight:',
    9: ':nine:'
}


def get_emoji_number(number: int):
    num_str = emoji_numbers[number]
    return emoji.emojize(num_str, language='alias')


def get_emoji_by_alias(alias: str):
    return emoji.emojize(f':{alias}:', language='alias')


def get_warning_emoji():
    return get_emoji_by_alias('warning')


def get_bang_emoji():
    return get_emoji_by_alias('bangbang')


def get_beach_emoji():
    return get_emoji_by_alias('beach_with_umbrella')
