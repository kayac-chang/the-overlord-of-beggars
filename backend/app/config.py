from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    OPEN_POINT_MID_V: str
    NEON_DB_URL: str
    OPENAI_API_KEY: str


settings = Settings()  # type: ignore
