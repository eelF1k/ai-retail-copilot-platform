from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AI Retail Copilot Platform"
    app_env: str = "dev"
    debug: bool = True
    api_prefix: str = "/api/v1"

    postgres_dsn: str = "postgresql+asyncpg://app:app@localhost:5432/retail_ai"
    redis_url: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

