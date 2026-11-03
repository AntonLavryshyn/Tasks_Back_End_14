from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "my_user"
    DB_PASS: str = "my_password"
    DB_NAME: str = "my_database"
    DATABASE_URL: Optional[str] = None

    @property
    def DATABASE_URL_asyncpg(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        case_sensetive=False
    )

settings = Settings()