from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

    OPENAI_API_KEY: str
    ELEVENLABS_API_KEY: str
    TELEGRAM_BOT_TOKEN: str


settings = Settings()
