from environs import Env
from dataclasses import dataclass


@dataclass
class BotConfig:
    token: str


@dataclass
class DbConfig:
    name: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class ImageGeneratorConfig:
    host: str
    port: int


@dataclass
class Config:
    bot_config: BotConfig
    db_config: DbConfig
    image_generator_config: ImageGeneratorConfig


def load_config():
    env = Env()
    env.read_env()

    return Config(
        bot_config=BotConfig(token=env.str("BALD_BOOKKEEPER_BOT_TOKEN")),
        db_config=DbConfig(
            name=env.str("DB_NAME"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
        ),
        image_generator_config=ImageGeneratorConfig(
            host=env.str("IMAGE_GENERATOR_API_URL"),
            port=env.int("IMAGE_GENERATOR_API_PORT"),
        ),
    )
