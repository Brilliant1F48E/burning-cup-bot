import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    admin_id: int
    use_redis: bool


@dataclass
class Path:
    images: str


@dataclass
class DbConfig:
    host: str
    user: str
    password: str
    db_name: str


@dataclass
class Config:
    tg_bot: TgBot
    path: Path
    db: DbConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]
    db = config["db"]
    path = config["path"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_id=tg_bot.getint('admin_id'),
            use_redis=tg_bot.getboolean('use_redis')
        ),
        path=Path(
            images=path.get("images")
        ),
        db=DbConfig(
            host=db.get('host'),
            user=db.get('user'),
            password=db.get('password'),
            db_name=db.get('db_name'),
        )
    )
