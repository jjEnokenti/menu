from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

__all__ = (
    'settings',
)

load_dotenv()


class Settings(BaseSettings):
    """App settings."""
    MODE: str = 'DEV'
    FILE_READ_MODE: str = 'LOCAL'

    BASE_DIR: str = Path(__file__).resolve().parent.parent.as_posix()
    ADMIN_FILE_PATH: str = f'{BASE_DIR}/admin/Menu.xlsx'

    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int = 5432

    REDIS_CACHE_EXPIRE: int
    REDIS_DB: int
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int = 5672
    CELERY_RESULT_BACKEND: str = 'rpc://'

    SPREADSHEET_ID: str
    CREDENTIALS_FILE: str = f'{BASE_DIR}/src/celery/credentials.json'

    @property
    def BROKER_URL(self) -> str:
        """Return broker url."""
        return (
            f'amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@'
            f'{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}//'
        )

    @property
    def DATABASE_URL(self) -> str:
        """Return db url."""
        return (
            f'postgresql+asyncpg://'
            f'{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    class ConfigDict:
        env_files = '.env'


settings = Settings()
