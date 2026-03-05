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
    def create_database():
        """
        Создание базы данных если она не существует.

        Подключается к стандартной базе postgres, проверяет наличие целевой БД
        и создает её при необходимости.

        Returns:
            bool: True если БД создана или уже существует, False в случае ошибки
        """
        try:
            # Подключение к стандартной базе postgres
            conn = psycopg2.connect(
                host=DBConfig.HOST,
                port=DBConfig.PORT,
                user=DBConfig.USER,
                password=DBConfig.PASSWORD,
                database='postgres'
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            # Проверка существования базы данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DBConfig.NAME,))
            exists = cur.fetchone()

            if not exists:
                cur.execute(sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DBConfig.NAME)
                ))
                print(f"База данных {DBConfig.NAME} успешно создана")
            else:
                print(f"База данных {DBConfig.NAME} уже существует")

            cur.close()
            conn.close()
            return True

        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")
            return False

    @staticmethod
    def create_tables():
        """
        Создание таблиц employers и vacancies.

        Создает две связанные таблицы:
        - employers: информация о компаниях-работодателях
        - vacancies: информация о вакансиях с внешним ключом на employers

        Также создает индексы для ускорения поиска.

        Returns:
            bool: True если таблицы созданы успешно, False в случае ошибки
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

            # Таблица компаний
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

            # Таблица вакансий
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

            # Индексы для ускорения поиска
            cur.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_employer ON vacancies(employer_id)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_salary ON vacancies(salary_from, salary_to)")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_vacancies_name ON vacancies(name)")

            conn.commit()
            print("Таблицы успешно созданы")
            cur.close()
            conn.close()
            return True

        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
            return False