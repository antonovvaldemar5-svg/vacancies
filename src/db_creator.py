"""
Модуль для создания базы данных и таблиц PostgreSQL.
"""
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.config import DBConfig


class DBCreator:
    """Класс для создания базы данных и таблиц."""

    @staticmethod
    def create_database() -> bool:
        """
        Создание базы данных если она не существует.

        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            conn = psycopg2.connect(
                host=DBConfig.HOST,
                port=DBConfig.PORT,
                user=DBConfig.USER,
                password=DBConfig.PASSWORD,
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DBConfig.NAME,))
            exists = cur.fetchone()

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DBConfig.NAME)
                ))
                print(f"База данных {DBConfig.NAME} создана")
            else:
                print(f"База данных {DBConfig.NAME} уже существует")

            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка создания БД: {e}")
            return False

    @staticmethod
    def create_tables() -> bool:
        """
        Создание таблиц employers и vacancies.

        Returns:
            bool: True если успешно, False если ошибка
        """
        try:
            conn = psycopg2.connect(
                host=DBConfig.HOST,
                port=DBConfig.PORT,
                database=DBConfig.NAME,
                user=DBConfig.USER,
                password=DBConfig.PASSWORD
            )
            cur = conn.cursor()

            cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id SERIAL PRIMARY KEY,
                    employer_id VARCHAR(50) UNIQUE NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    site_url VARCHAR(255),
                    logo_url VARCHAR(255),
                    hh_url VARCHAR(255)
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id SERIAL PRIMARY KEY,
                    vacancy_id VARCHAR(50) UNIQUE NOT NULL,
                    employer_id VARCHAR(50) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    salary_currency VARCHAR(10),
                    url VARCHAR(255),
                    experience VARCHAR(100),
                    published_at TIMESTAMP,
                    FOREIGN KEY (employer_id) 
                        REFERENCES employers(employer_id) 
                        ON DELETE CASCADE
                )
            """)

            cur.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_employer ON vacancies(employer_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_salary ON vacancies(salary_from, salary_to)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_name ON vacancies(name)")

            conn.commit()
            print("Таблицы созданы успешно")
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"Ошибка создания таблиц: {e}")
            return False
