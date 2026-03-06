"""
Модуль для работы с API HeadHunter.
"""
import requests
import re
from typing import List, Dict, Any, Optional
from .abstract_classes import APIHandler


class HeadHunterAPI(APIHandler):
    """Класс для работы с API HeadHunter."""

    def __init__(self):
        """Инициализация API клиента."""
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {
            "User-Agent": "HH-User-Agent"
        }

    def get_vacancies(self, search_query: str, per_page: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу.

        Args:
            search_query: Поисковый запрос
            per_page: Количество вакансий на странице
            **kwargs: Дополнительные параметры

        Returns:
            Список вакансий
        """
        params = {
            "text": search_query,
            "per_page": per_page,
            "area": 113,
            "page": kwargs.get("page", 0),
            "only_with_salary": kwargs.get("only_with_salary", False)
        }

        try:
            response = requests.get(self._base_url, headers=self._headers, params=params)
            response.raise_for_status()
            data = response.json()

            vacancies = []
            for item in data.get("items", []):
                salary_data = item.get("salary")
                salary_from = None
                salary_to = None
                salary_currency = None

                if salary_data:
                    salary_from = salary_data.get("from")
                    salary_to = salary_data.get("to")
                    salary_currency = salary_data.get("currency")

                vacancy = {
                    "id": item.get("id", ""),
                    "name": item.get("name", ""),
                    "url": item.get("alternate_url", ""),
                    "salary_from": salary_from,
                    "salary_to": salary_to,
                    "salary_currency": salary_currency,
                    "description": self._clean_description(item.get("snippet", {}).get("requirement", "")),
                    "experience": item.get("experience", {}).get("name", ""),
                    "employer": item.get("employer", {}).get("name", ""),
                    "published_at": item.get("published_at", "")
                }
                vacancies.append(vacancy)

            return vacancies

        except requests.RequestException as e:
            print(f"Ошибка при получении вакансий: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return []

    def search_companies(self, company_name: str, per_page: int = 10) -> List[Dict[str, Any]]:
        """
        Поиск компаний по названию.

        Args:
            company_name: Название компании
            per_page: Количество результатов

        Returns:
            Список компаний
        """
        url = "https://api.hh.ru/employers"
        params = {
            "text": company_name,
            "per_page": per_page,
            "area": 113
        }

        try:
            response = requests.get(url, headers=self._headers, params=params)
            response.raise_for_status()
            data = response.json()

            companies = []
            for item in data.get("items", []):
                company = {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "description": item.get("description"),
                    "site_url": item.get("site_url"),
                    "logo_url": item.get("logo", {}).get("original") if item.get("logo") else None,
                    "hh_url": item.get("alternate_url")
                }
                companies.append(company)
            return companies
        except Exception as e:
            print(f"Ошибка поиска компаний: {e}")
            return []

    def get_company_vacancies(self, employer_id: str, per_page: int = 100) -> List[Dict[str, Any]]:
        """
        Получение вакансий компании.

        Args:
            employer_id: ID компании
            per_page: Количество вакансий

        Returns:
            Список вакансий компании
        """
        params = {
            "employer_id": employer_id,
            "per_page": per_page,
            "area": 113,
            "only_with_salary": False
        }

        try:
            response = requests.get(self._base_url, headers=self._headers, params=params)
            response.raise_for_status()
            data = response.json()

            vacancies = []
            for item in data.get("items", []):
                salary = item.get("salary")
                vacancy = {
                    "id": item.get("id"),
                    "name": item.get("name"),
                    "description": self._clean_description(item.get("snippet", {}).get("requirement", "")),
                    "salary_from": salary.get("from") if salary else None,
                    "salary_to": salary.get("to") if salary else None,
                    "salary_currency": salary.get("currency") if salary else None,
                    "url": item.get("alternate_url"),
                    "experience": item.get("experience", {}).get("name"),
                    "published_at": item.get("published_at")
                }
                vacancies.append(vacancy)
            return vacancies
        except Exception as e:
            print(f"Ошибка получения вакансий компании: {e}")
            return []

    @staticmethod
    def _clean_description(description: str) -> str:
        """Очистка описания от HTML-тегов."""
        if not description:
            return ""
        return re.sub(r'<[^>]+>', '', description)
