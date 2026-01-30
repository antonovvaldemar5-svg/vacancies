import pytest
from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def test_vacancy_creation(self):
        """Тест создания вакансии"""
        vacancy = Vacancy(
            _id="123",
            _name="Python Developer",
            _url="https://hh.ru/vacancy/123",
            _salary_from=100000,
            _salary_to=150000,
            _salary_currency="RUR",
            _description="Требуется Python разработчик",
            _experience="1-3 года",
            _employer="Test Company"
        )

        assert vacancy._name == "Python Developer"
        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.avg_salary == 125000

    def test_vacancy_comparison(self):
        """Тест сравнения вакансий по зарплате"""
        vacancy1 = Vacancy(
            _id="1",
            _name="Junior",
            _url="url1",
            _salary_from=50000,
            _salary_to=70000
        )

        vacancy2 = Vacancy(
            _id="2",
            _name="Senior",
            _url="url2",
            _salary_from=150000,
            _salary_to=200000
        )

        vacancy3 = Vacancy(
            _id="3",
            _name="Middle",
            _url="url3",
            _salary_from=100000,
            _salary_to=120000
        )

        # Сравнения
        assert vacancy2 > vacancy1
        assert vacancy1 < vacancy2
        assert vacancy2 >= vacancy3
        assert vacancy1 <= vacancy3
        assert vacancy2 != vacancy1

        # Сортировка списка
        vacancies = [vacancy1, vacancy2, vacancy3]
        sorted_vacancies = sorted(vacancies, reverse=True)
        assert sorted_vacancies[0] == vacancy2
        assert sorted_vacancies[1] == vacancy3
        assert sorted_vacancies[2] == vacancy1

    def test_vacancy_without_salary(self):
        """Тест вакансии без зарплаты"""
        vacancy = Vacancy(
            _id="123",
            _name="Python Developer",
            _url="https://hh.ru/vacancy/123"
        )

        assert vacancy.salary_from == 0
        assert vacancy.salary_to == 0
        assert vacancy.avg_salary == 0.0
        assert vacancy.formatted_salary == "Зарплата не указана"

    def test_formatted_salary(self):
        """Тест форматирования зарплаты"""
        # Только от
        vacancy1 = Vacancy(
            _id="1",
            _name="Test",
            _url="url1",
            _salary_from=100000,
            _salary_currency="RUR"
        )
        assert "от 100000" in vacancy1.formatted_salary

        # Только до
        vacancy2 = Vacancy(
            _id="2",
            _name="Test",
            _url="url2",
            _salary_to=150000,
            _salary_currency="RUR"
        )
        assert "до 150000" in vacancy2.formatted_salary

        # От и до
        vacancy3 = Vacancy(
            _id="3",
            _name="Test",
            _url="url3",
            _salary_from=100000,
            _salary_to=150000,
            _salary_currency="RUR"
        )
        assert "от 100000 до 150000 RUR" == vacancy3.formatted_salary

    def test_to_dict_from_dict(self):
        """Тест преобразования в словарь и обратно"""
        vacancy = Vacancy(
            _id="123",
            _name="Python Developer",
            _url="https://hh.ru/vacancy/123",
            _salary_from=100000,
            _salary_to=150000,
            _description="Test description",
            _employer="Test Company"
        )

        # В словарь
        data = vacancy.to_dict()
        assert data["id"] == "123"
        assert data["name"] == "Python Developer"
        assert data["salary_from"] == 100000

        # Из словаря (из формата HH.ru)
        hh_data = {
            "id": "456",
            "name": "Java Developer",
            "url": "https://hh.ru/vacancy/456",
            "salary": {
                "from": 80000,
                "to": 120000,
                "currency": "RUR"
            },
            "description": "Java разработчик",
            "experience": "От 1 года",
            "employer": "Another Company"
        }

        vacancy_from_dict = Vacancy.from_dict(hh_data)
        assert vacancy_from_dict._id == "456"
        assert vacancy_from_dict._name == "Java Developer"
        assert vacancy_from_dict._salary_from == 80000
        assert vacancy_from_dict._salary_to == 120000

    def test_cast_to_object_list(self):
        """Тест преобразования списка словарей в список объектов"""
        data_list = [
            {
                "id": "1",
                "name": "Python",
                "url": "url1",
                "salary": {"from": 100000, "to": 150000}
            },
            {
                "id": "2",
                "name": "Java",
                "url": "url2",
                "salary": {"from": 80000, "to": 120000}
            }
        ]

        vacancies = Vacancy.cast_to_object_list(data_list)

        assert len(vacancies) == 2
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0]._name == "Python"
        assert vacancies[1]._name == "Java"
        