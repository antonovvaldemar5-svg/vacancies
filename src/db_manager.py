"""
Модуль для работы с данными в PostgreSQL.
"""
from typing import List, Dict, Any, Optional, Union
import psycopg2
from psycopg2.extras import RealDictCursor
from src.config import DBConfig


class DBManager:
    """Класс для работы с данными в PostgreSQL."""

    def __init__(self) -> None:
        """Инициализация подключения к базе данных."""
        self.conn = psycopg2.connect(
            host=DBConfig.HOST,
            port=DBConfig.PORT,
            database=DBConfig.NAME,
            user=DBConfig.USER,
            password=DBConfig.PASSWORD,
            cursor_factory=RealDictCursor
        )

    def _execute_query(self, query: str, params: Optional[tuple] = None,
                       fetch: bool = True) -> Optional[List[Dict[str, Any]]]:
        """
        Выполнение SQL запроса.

        Args:
            query: SQL запрос
            params: Параметры запроса
            fetch: Нужно ли возвращать результаты

        Returns:
            Результаты запроса если fetch=True, иначе None
        """
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                return cur.fetchall()
            self.conn.commit()
            return None

    def insert_employer(self, employer_data: Dict[str, Any]) -> None:
        """
        Вставка данных о компании.

        Args:
            employer_data: Словарь с данными компании
        """
        query = """
            INSERT INTO employers 
                (employer_id, name, description, site_url, logo_url, hh_url)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (employer_id) DO NOTHING
        """
        params = (
            employer_data['id'],
            employer_data['name'],
            employer_data.get('description'),
            employer_data.get('site_url'),
            employer_data.get('logo_url'),
            employer_data.get('hh_url', '')
        )
        self._execute_query(query, params, fetch=False)

    def insert_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """
        Вставка данных о вакансии.

        Args:
            vacancy_data: Словарь с данными вакансии
        """
        query = """
            INSERT INTO vacancies 
                (vacancy_id, employer_id, name, description, 
                 salary_from, salary_to, salary_currency, 
                 url, experience, published_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (vacancy_id) DO NOTHING
        """
        params = (
            vacancy_data['id'],
            vacancy_data['employer_id'],
            vacancy_data['name'],
            vacancy_data.get('description'),
            vacancy_data.get('salary_from'),
            vacancy_data.get('salary_to'),
            vacancy_data.get('salary_currency'),
            vacancy_data['url'],
            vacancy_data.get('experience'),
            vacancy_data.get('published_at')
        )
        self._execute_query(query, params, fetch=False)

    def get_companies_and_vacancies_count(self) -> List[Dict[str, Union[str, int]]]:
        """
        Получение списка компаний и количества вакансий.

        Returns:
            Список словарей с ключами:
                - company_name: str - название компании
                - vacancies_count: int - количество вакансий
        """
        query = """
            SELECT 
                e.name AS company_name,
                COUNT(v.id) AS vacancies_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name, e.employer_id
            ORDER BY vacancies_count DESC
        """
        return self._execute_query(query) or []

    def get_all_vacancies(self) -> List[Dict[str, Any]]:
        """
        Получение всех вакансий с деталями.

        Returns:
            Список словарей с ключами:
                - company_name: str
                - vacancy_name: str
                - salary_from: Optional[int]
                - salary_to: Optional[int]
                - salary_currency: Optional[str]
                - url: str
        """
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
        return self._execute_query(query) or []

    def get_avg_salary(self) -> Optional[float]:
        """
        Получение средней зарплаты.

        Returns:
            Средняя зарплата или None если нет данных
        """
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
        return result[0]['avg_salary'] if result and result[0]['avg_salary'] else None

    def get_vacancies_with_higher_salary(self) -> List[Dict[str, Any]]:
        """
        Получение вакансий с зарплатой выше средней.

        Returns:
            Список вакансий
        """
        avg_salary = self.get_avg_salary()
        if not avg_salary:
            return []

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
        return self._execute_query(query, (avg_salary,)) or []

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        Поиск вакансий по ключевому слову.

        Args:
            keyword: Ключевое слово для поиска

        Returns:
            Список вакансий
        """
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
        return self._execute_query(query, (f'%{keyword.lower()}%',)) or []

    def close(self) -> None:
        """Закрытие соединения с базой данных."""
        if self.conn:
            self.conn.close()
