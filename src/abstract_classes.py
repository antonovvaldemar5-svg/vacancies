from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class APIHandler(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def get_vacancies(self, search_query: str, **kwargs) -> List[Dict[str, Any]]:
        """Получение вакансий по поисковому запросу"""


class FileHandler(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Добавление вакансии в файл"""

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Получение вакансий из файла по критериям"""

    @abstractmethod
    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаление вакансии из файла"""

    @abstractmethod
    def clear_file(self) -> None:
        """Очистка файла"""
