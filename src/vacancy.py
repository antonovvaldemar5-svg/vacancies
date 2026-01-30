from __future__ import annotations

from typing import Any, Dict, List, Optional


class Vacancy:
    """Класс для представления вакансии"""

    def __init__(
            self,
            _id: str,
            _name: str,
            _url: str,
            _salary_from: Optional[int] = None,
            _salary_to: Optional[int] = None,
            _salary_currency: Optional[str] = None,
            _description: Optional[str] = None,
            _experience: Optional[str] = None,
            _employer: Optional[str] = None,
            _published_at: Optional[str] = None,
    ):
        """Инициализация вакансии"""
        self._id = _id
        self._name = _name
        self._url = _url
        self._salary_from = _salary_from
        self._salary_to = _salary_to
        self._salary_currency = _salary_currency
        self._description = _description
        self._experience = _experience
        self._employer = _employer
        self._published_at = _published_at

        self._validate_data()

    def _validate_data(self):
        """Приватный метод для валидации данных"""
        if not self._name:
            raise ValueError("Название вакансии не может быть пустым")

        if self._salary_from is not None and self._salary_from < 0:
            self._salary_from = 0

        if self._salary_to is not None and self._salary_to < 0:
            self._salary_to = 0

        if self._salary_from is not None and self._salary_to is not None:
            if self._salary_from > self._salary_to:
                self._salary_from, self._salary_to = self._salary_to, self._salary_from

    @property
    def salary_from(self) -> int:
        """Возвращает начальную зарплату"""
        return self._salary_from or 0

    @property
    def salary_to(self) -> int:
        """Возвращает конечную зарплату"""
        return self._salary_to or 0

    @property
    def avg_salary(self) -> float:
        """Возвращает среднюю зарплату"""
        if self._salary_from and self._salary_to:
            return (self._salary_from + self._salary_to) / 2
        elif self._salary_from:
            return float(self._salary_from)
        elif self._salary_to:
            return float(self._salary_to)
        return 0.0

    @property
    def formatted_salary(self) -> str:
        """Возвращает отформатированную строку зарплаты"""
        if not self._salary_from and not self._salary_to:
            return "Зарплата не указана"

        parts = []
        if self._salary_from:
            parts.append(f"от {self._salary_from:,}")
        if self._salary_to:
            parts.append(f"до {self._salary_to:,}")

        salary_str = " ".join(parts)
        if self._salary_currency:
            salary_str += f" {self._salary_currency}"

        return salary_str.replace(",", " ")

    def __str__(self) -> str:
        """Строковое представление вакансии"""
        lines = [
            f"Вакансия: {self._name}",
            f"Компания: {self._employer or 'Не указано'}",
            f"Зарплата: {self.formatted_salary}",
            f"Опыт: {self._experience or 'Не указан'}",
            f"Ссылка: {self._url}",
        ]

        if self._description:
            desc = (
                self._description[:100] + "..."
                if len(self._description) > 100
                else self._description
            )
            lines.append(f"Описание: {desc}")

        return "\n".join(lines)

    # Методы сравнения по зарплате
    def __lt__(self, other: Vacancy) -> bool:
        return self.avg_salary < other.avg_salary

    def __le__(self, other: Vacancy) -> bool:
        return self.avg_salary <= other.avg_salary

    def __gt__(self, other: Vacancy) -> bool:
        return self.avg_salary > other.avg_salary

    def __ge__(self, other: Vacancy) -> bool:
        return self.avg_salary >= other.avg_salary

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование вакансии в словарь"""
        return {
            "id": self._id,
            "name": self._name,
            "url": self._url,
            "salary_from": self._salary_from,
            "salary_to": self._salary_to,
            "salary_currency": self._salary_currency,
            "description": self._description,
            "experience": self._experience,
            "employer": self._employer,
            "published_at": self._published_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Vacancy:
        """Создание вакансии из словаря"""
        # Обработка зарплаты из формата HH.ru
        salary = data.get("salary")
        salary_from = data.get("salary_from")
        salary_to = data.get("salary_to")
        salary_currency = data.get("salary_currency")

        if salary and not salary_from:
            salary_from = salary.get("from")
            salary_to = salary.get("to")
            salary_currency = salary.get("currency")

        # Получаем URL из разных полей
        url = data.get("url") or data.get("alternate_url") or ""

        return cls(
            _id=data.get("id", ""),
            _name=data.get("name", ""),
            _url=url,
            _salary_from=salary_from,
            _salary_to=salary_to,
            _salary_currency=salary_currency,
            _description=data.get("description"),
            _experience=data.get("experience"),
            _employer=data.get("employer"),
            _published_at=data.get("published_at"),
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict[str, Any]]) -> List[Vacancy]:
        """Преобразование списка словарей в список объектов Vacancy"""
        return [cls.from_dict(data) for data in vacancies_data]
