from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Defaults apply only when no .env file is present.
    # In any deployed environment these are overridden by real .env values.
    DATABASE_URL: str = "sqlite:///./addressbook.db"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    API_VERSION: str = "v1"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
