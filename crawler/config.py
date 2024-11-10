from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str
    FAMILY_MART_KEY: str
    OPENAI_API_KEY: str
    MEILISEARCH_URL: str
    MEILI_MASTER_KEY: str


settings = Settings()  # type: ignore
