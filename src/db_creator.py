import psycopg2
from src.config import DBConfig


class DBCreator:
    """Создание базы данных и таблиц"""

    @staticmethod
    def create_tables():
        """Создание таблиц employers и vacancies"""
        try:
            conn = psycopg2.connect(
                host=DBConfig.HOST,
                port=DBConfig.PORT,
                database=DBConfig.NAME,
                user=DBConfig.USER,
                password=DBConfig.PASSWORD,
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

            conn.commit()
            print("Таблицы созданы успешно")
            cur.close()
            conn.close()
            return True

        except Exception as e:
            print(f"Ошибка создания таблиц: {e}")
            return False
