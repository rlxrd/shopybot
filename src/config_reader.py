from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE_LOCATION = Path(".env").resolve()


class Settings(BaseSettings):
    ADMIN_IDS: list[int] = [1490170564]

    BOT_TOKEN: SecretStr
    DATABASE_URL: SecretStr

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_LOCATION,
        env_file_encoding="utf-8"
    )


config = Settings()