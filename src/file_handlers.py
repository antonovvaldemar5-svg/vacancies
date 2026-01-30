import json
import os
from typing import Any, Dict, List, Optional

from .abstract_classes import FileHandler


class JSONSaver(FileHandler):
    """Класс для работы с JSON-файлами"""

    def __init__(self, filename: str = "vacancies.json"):
        self._filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Создание файла, если он не существует"""
        if not os.path.exists(self._filename):
            with open(self._filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_file(self) -> List[Dict[str, Any]]:
        """Чтение данных из файла"""
        try:
            with open(self._filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_file(self, data: List[Dict[str, Any]]) -> None:
        """Запись данных в файл"""
        with open(self._filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Добавление вакансии в файл (без дубликатов)"""
        vacancies = self._read_file()

        vacancy_id = vacancy_data.get("id")
        if any(v.get("id") == vacancy_id for v in vacancies):
            return

        vacancies.append(vacancy_data)
        self._write_file(vacancies)

    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Получение вакансий по критериям"""
        vacancies = self._read_file()

        if not criteria:
            return vacancies

        filtered_vacancies = []
        for vacancy in vacancies:
            match = True

            for key, value in criteria.items():
                if key in vacancy:
                    vacancy_value = vacancy[key]

                    if isinstance(value, str) and isinstance(vacancy_value, str):
                        if value.lower() not in vacancy_value.lower():
                            match = False
                            break
                    elif vacancy_value != value:
                        match = False
                        break

            if match:
                filtered_vacancies.append(vacancy)

        return filtered_vacancies

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Удаление вакансии по ID"""
        vacancies = self._read_file()
        vacancies = [v for v in vacancies if v.get("id") != vacancy_id]
        self._write_file(vacancies)

    def clear_file(self) -> None:
        """Очистка файла (удаление всех вакансий)"""
        self._write_file([])


class CSVSaver(FileHandler):
    """Класс для работы с CSV-файлами"""

    def __init__(self, filename: str = "vacancies.csv"):
        self._filename = filename

    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("CSVSaver.add_vacancy еще не реализован")

    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("CSVSaver.get_vacancies еще не реализован")

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("CSVSaver.delete_vacancy еще не реализован")

    def clear_file(self) -> None:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("CSVSaver.clear_file еще не реализован")


class TXTSaver(FileHandler):
    """Класс для работы с TXT-файлами"""

    def __init__(self, filename: str = "vacancies.txt"):
        self._filename = filename

    def add_vacancy(self, vacancy_data: Dict[str, Any]) -> None:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("TXTSaver.add_vacancy еще не реализован")

    def get_vacancies(
        self, criteria: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("TXTSaver.get_vacancies еще не реализован")

    def delete_vacancy(self, vacancy_id: str) -> None:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("TXTSaver.delete_vacancy еще не реализован")

    def clear_file(self) -> None:
        """Заглушка - метод не реализован"""
        raise NotImplementedError("TXTSaver.clear_file еще не реализован")
