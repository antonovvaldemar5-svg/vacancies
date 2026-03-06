import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    """Конфигурация для подключения к БД"""

    HOST = os.getenv("DB_HOST", "localhost")
    PORT = os.getenv("DB_PORT", "5432")
    NAME = os.getenv("DB_NAME", "hh_vacancies")
    USER = os.getenv("DB_USER", "postgres")
    PASSWORD = os.getenv("DB_PASSWORD", "")
