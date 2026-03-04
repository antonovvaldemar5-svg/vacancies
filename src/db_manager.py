import psycopg2
from psycopg2.extras import RealDictCursor
from src.config import DBConfig


class DBManager:
    """Класс для работы с данными в PostgreSQL"""

    def __init__(self):
        """Подключение к БД"""
        self.conn = psycopg2.connect(
            host=DBConfig.HOST,
            port=DBConfig.PORT,
            database=DBConfig.NAME,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD,
            cursor_factory=RealDictCursor,
        )

    def _execute_query(self, query, params=None, fetch=True):
        """Выполнение SQL запроса"""
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            self.conn.commit()
            return None

    def insert_employer(self, employer_data):
        """Вставка компании"""
        query = """
            INSERT INTO employers
                (employer_id, name, description, site_url, logo_url, hh_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (employer_id) DO NOTHING
        """
        params = (
            employer_data["id"],
            employer_data["name"],
            employer_data.get("description"),
            employer_data.get("site_url"),
            employer_data.get("logo_url"),
            employer_data.get("hh_url", ""),
        )
        self._execute_query(query, params, fetch=False)

    def insert_vacancy(self, vacancy_data):
        """Вставка вакансии"""
        query = """
            INSERT INTO vacancies
                (vacancy_id, employer_id, name, description,
                 salary_from, salary_to, salary_currency,
                 url, experience, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
        """
        params = (
            vacancy_data["id"],
            vacancy_data["employer_id"],
            vacancy_data["name"],
            vacancy_data.get("description"),
            vacancy_data.get("salary_from"),
            vacancy_data.get("salary_to"),
            vacancy_data.get("salary_currency"),
            vacancy_data["url"],
            vacancy_data.get("experience"),
            vacancy_data.get("published_at"),
        )
        self._execute_query(query, params, fetch=False)

    def get_companies_and_vacancies_count(self):
        """Список компаний и количество вакансий"""
        query = """
            SELECT
                e.name AS company_name,
                COUNT(v.id) AS vacancies_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name, e.employer_id
            ORDER BY vacancies_count DESC
        """
        return self._execute_query(query)

    def get_all_vacancies(self):
        """Все вакансии с компаниями"""
        query = """
            SELECT
                e.name AS company_name,
                v.name AS vacancy_name,
                v.salary_from,
                v.salary_to,
                v.salary_currency,
                v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            ORDER BY e.name, v.name
        """
        return self._execute_query(query)

    def get_avg_salary(self):
        """Средняя зарплата"""
        query = """
            SELECT
                ROUND(AVG(
                    CASE
                        WHEN salary_from IS NOT NULL AND salary_to IS NOT NULL
                            THEN (salary_from + salary_to) / 2.0
                        WHEN salary_from IS NOT NULL THEN salary_from
                        WHEN salary_to IS NOT NULL THEN salary_to
                        ELSE NULL
                    END
                )) AS avg_salary
            FROM vacancies
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
        """
        result = self._execute_query(query)
        return result[0]["avg_salary"] if result else 0

    def get_vacancies_with_higher_salary(self):
        """Вакансии с зарплатой выше средней"""
        avg_salary = self.get_avg_salary()

        query = """
            SELECT
                e.name AS company_name,
                v.name AS vacancy_name,
                v.salary_from,
                v.salary_to,
                v.salary_currency,
                v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE
                CASE
                    WHEN v.salary_from IS NOT NULL AND v.salary_to IS NOT NULL
                        THEN (v.salary_from + v.salary_to) / 2.0
                    WHEN v.salary_from IS NOT NULL THEN v.salary_from
                    WHEN v.salary_to IS NOT NULL THEN v.salary_to
                    ELSE NULL
                END > %s
            ORDER BY e.name
        """
        return self._execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword):
        """Поиск по ключевому слову"""
        query = """
            SELECT
                e.name AS company_name,
                v.name AS vacancy_name,
                v.salary_from,
                v.salary_to,
                v.salary_currency,
                v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.name) LIKE %s
            ORDER BY e.name, v.name
        """
        return self._execute_query(query, (f"%{keyword.lower()}%",))

    def close(self):
        """Закрытие соединения"""
        if self.conn:
            self.conn.close()
