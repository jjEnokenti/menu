import os

from dotenv import load_dotenv


__all__ = (
    'settings',
    'test_settings',
)

load_dotenv()


class BaseConfig:
    """Base config."""
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    DATABASE_URL = (f'postgresql+asyncpg://'
                    f'{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


class TestConfig:
    """Test config."""
    DB_USER = os.getenv('DB_USER', 'test')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'test')
    DB_HOST = os.getenv('TEST_DB_HOST', 'test_db')
    DB_NAME = os.getenv('TEST_DB_NAME', 'test_menu_db')

    DATABASE_URL = (f'postgresql+asyncpg://'
                    f'{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


settings = BaseConfig()
test_settings = TestConfig()
