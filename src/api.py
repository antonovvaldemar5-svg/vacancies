import requests
import re
from typing import List, Dict, Any
from .abstract_classes import APIHandler


class HeadHunterAPI(APIHandler):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self._base_url = "https://api.hh.ru/vacancies"
        self._headers = {
            "User-Agent": "HH-User-Agent"
        }

    def get_vacancies(self, search_query: str, per_page: int = 100, **kwargs) -> List[Dict[str, Any]]:
        """
        Получение вакансий по поисковому запросу

        Args:
            search_query: Поисковый запрос
            per_page: Количество вакансий на странице
            **kwargs: Дополнительные параметры

        Returns:
            Список вакансий в формате словарей
        """
        params = {
            "text": search_query,
            "per_page": per_page,
            "area": 113,  # Россия
            "page": kwargs.get("page", 0),
            "only_with_salary": kwargs.get("only_with_salary", False)
        }

        try:
            response = requests.get(self._base_url, headers=self._headers, params=params)
            response.raise_for_status()
            data = response.json()

            vacancies = []
            for item in data.get("items", []):
                # Получаем зарплату
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

    @staticmethod
    def _clean_description(description: str) -> str:
        """Очистка описания от HTML-тегов"""
        if not description:
            return ""
        return re.sub(r'<[^>]+>', '', description)
