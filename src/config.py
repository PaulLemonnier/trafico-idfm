from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    IDFM_API_KEY: SecretStr = Field(validation_alias="IDFM_API_KEY")
    TELEGRAM_BOT_TOKEN: SecretStr = Field(validation_alias="TELEGRAM_BOT_TOKEN")
    API_URL: str = Field(validation_alias="API_URL")
    API_KEY: SecretStr = Field(validation_alias="API_KEY")
    ALLOWED_CHAT_ID: str = Field(validation_alias="ALLOWED_CHAT_ID")
    RB_USER: str = Field(validation_alias="RB_USER")
    RB_HOSTNAME: str = Field(validation_alias="RB_HOSTNAME")
    RB_PASSWORD: SecretStr = Field(validation_alias="RB_PASSWORD")
    RB_HOST: str = Field(validation_alias="RB_HOST")


    # Configuration pour indiquer où trouver le fichier .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Config()