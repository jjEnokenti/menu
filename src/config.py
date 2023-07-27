from dotenv import load_dotenv
from pydantic_settings import BaseSettings


__all__ = (
    'settings',
)

load_dotenv()


class Settings(BaseSettings):
    """App settings."""
    MODE: str

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    DB_PORT: int

    @property
    def DATABASE_URL(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    class ConfigDict:
        env_files = '.env'


settings = Settings()
