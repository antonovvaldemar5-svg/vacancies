import pytest
from src.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.vacancy_data = {
            "_id": "123",
            "_name": "Python Developer",
            "_url": "https://hh.ru/vacancy/123",
            "_salary_from": 100000,
            "_salary_to": 150000,
            "_salary_currency": "RUR",
            "_description": "Разработка на Python, Django",
            "_experience": "От 1 года до 3 лет",
            "_employer": "Test Company",
            "_published_at": "2024-01-01T10:00:00+0300",
        }

    def test_init_valid_data(self):
        """Тест инициализации с валидными данными"""
        vacancy = Vacancy(**self.vacancy_data)

        assert vacancy._id == "123"
        assert vacancy._name == "Python Developer"
        assert vacancy._url == "https://hh.ru/vacancy/123"
        assert vacancy._salary_from == 100000
        assert vacancy._salary_to == 150000
        assert vacancy._description == "Разработка на Python, Django"

    def test_init_without_salary(self):
        """Тест инициализации без зарплаты"""
        data = self.vacancy_data.copy()
        data.update({"_salary_from": None, "_salary_to": None, "_salary_currency": None})

        vacancy = Vacancy(**data)

        assert vacancy._salary_from is None
        assert vacancy._salary_to is None
        assert vacancy.salary_from == 0
        assert vacancy.salary_to == 0

    def test_init_negative_salary(self):
        """Тест с отрицательной зарплатой"""
        data = self.vacancy_data.copy()
        data["_salary_from"] = -1000
        data["_salary_to"] = -500

        vacancy = Vacancy(**data)

        assert vacancy._salary_from == 0
        assert vacancy._salary_to == 0

    def test_init_salary_from_greater_than_to(self):
        """Тест когда salary_from > salary_to"""
        data = self.vacancy_data.copy()
        data["_salary_from"] = 200000
        data["_salary_to"] = 100000

        vacancy = Vacancy(**data)

        assert vacancy._salary_from == 100000
        assert vacancy._salary_to == 200000

    def test_init_empty_name(self):
        """Тест с пустым названием"""
        data = self.vacancy_data.copy()
        data["_name"] = ""

        with pytest.raises(ValueError, match="Название вакансии не может быть пустым"):
            Vacancy(**data)

    def test_properties(self):
        """Тест свойств вакансии"""
        vacancy = Vacancy(**self.vacancy_data)

        assert vacancy.salary_from == 100000
        assert vacancy.salary_to == 150000
        assert vacancy.avg_salary == 125000.0

    def test_avg_salary_calculations(self):
        """Тест расчетов средней зарплаты"""
        # Только from
        vacancy1 = Vacancy(_id="1", _name="Test", _url="url", _salary_from=100000)
        assert vacancy1.avg_salary == 100000.0

        # Только to
        vacancy2 = Vacancy(_id="2", _name="Test", _url="url", _salary_to=150000)
        assert vacancy2.avg_salary == 150000.0

        # Нет зарплаты
        vacancy3 = Vacancy(_id="3", _name="Test", _url="url")
        assert vacancy3.avg_salary == 0.0

    def test_formatted_salary(self):
        """Тест форматирования зарплаты"""
        # Полная зарплата
        vacancy1 = Vacancy(**self.vacancy_data)
        assert "от 100 000" in vacancy1.formatted_salary
        assert "до 150 000" in vacancy1.formatted_salary
        assert "RUR" in vacancy1.formatted_salary

        # Только от
        vacancy2 = Vacancy(_id="2", _name="Test", _url="url", _salary_from=100000, _salary_currency="RUR")
        assert vacancy2.formatted_salary == "от 100 000 RUR"

        # Только до
        vacancy3 = Vacancy(_id="3", _name="Test", _url="url", _salary_to=150000, _salary_currency="USD")
        assert vacancy3.formatted_salary == "до 150 000 USD"

        # Без зарплаты
        vacancy4 = Vacancy(_id="4", _name="Test", _url="url")
        assert vacancy4.formatted_salary == "Зарплата не указана"

    def test_str_method(self):
        """Тест строкового представления"""
        vacancy = Vacancy(**self.vacancy_data)
        result = str(vacancy)

        assert "Python Developer" in result
        assert "Test Company" in result
        assert "от 100 000" in result
        assert "до 150 000" in result
        assert "https://hh.ru/vacancy/123" in result

    def test_str_method_with_long_description(self):
        """Тест строкового представления с длинным описанием"""
        long_desc = "a" * 150
        data = self.vacancy_data.copy()
        data["_description"] = long_desc

        vacancy = Vacancy(**data)
        result = str(vacancy)

        assert "..." in result
        # 100 символов + "..."
        assert len(result.split("Описание: ")[1]) <= 103

    def test_comparison_methods(self):
        """Тест методов сравнения"""
        vacancy1 = Vacancy(_id="1", _name="A", _url="url1", _salary_from=100000, _salary_to=150000)
        vacancy2 = Vacancy(_id="2", _name="B", _url="url2", _salary_from=120000, _salary_to=180000)
        vacancy3 = Vacancy(_id="1", _name="A", _url="url1", _salary_from=100000, _salary_to=150000)

        assert vacancy1 < vacancy2
        assert vacancy2 > vacancy1
        assert vacancy1 <= vacancy2
        assert vacancy2 >= vacancy1
        assert vacancy1 == vacancy3
        assert vacancy1 != vacancy2

    def test_hash_method(self):
        """Тест хэширования"""
        vacancy1 = Vacancy(_id="1", _name="Test", _url="url")
        vacancy2 = Vacancy(_id="1", _name="Test", _url="url")
        vacancy3 = Vacancy(_id="2", _name="Test", _url="url")

        assert hash(vacancy1) == hash(vacancy2)
        assert hash(vacancy1) != hash(vacancy3)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        vacancy = Vacancy(**self.vacancy_data)
        result = vacancy.to_dict()

        assert result["id"] == "123"
        assert result["name"] == "Python Developer"
        assert result["salary_from"] == 100000
        assert result["salary_to"] == 150000
        assert result["description"] == "Разработка на Python, Django"

    def test_from_dict_hh_format(self):
        """Тест создания из словаря в формате HH"""
        hh_data = {
            "id": "123",
            "name": "Python Developer",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "snippet": {"requirement": "Опыт работы"},
            "experience": {"name": "От 1 года до 3 лет"},
            "employer": {"name": "Test Company"},
            "published_at": "2024-01-01T10:00:00+0300",
        }

        vacancy = Vacancy.from_dict(hh_data)

        assert vacancy._id == "123"
        assert vacancy._name == "Python Developer"
        assert vacancy._url == "https://hh.ru/vacancy/123"
        assert vacancy._salary_from == 100000
        assert vacancy._salary_to == 150000
        assert vacancy._salary_currency == "RUR"

    def test_from_dict_direct_format(self):
        """Тест создания из прямого словаря"""
        data = {
            "id": "123",
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000,
            "salary_currency": "RUR",
            "description": "Test",
            "experience": "1-3 years",
            "employer": "Test Company",
            "published_at": "2024-01-01",
        }

        vacancy = Vacancy.from_dict(data)
        assert vacancy._name == "Python Developer"

    def test_cast_to_object_list(self):
        """Тест преобразования списка словарей"""
        data_list = [
            {
                "id": "1",
                "name": "Python Developer",
                "url": "url1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            },
            {
                "id": "2",
                "name": "Java Developer",
                "url": "url2",
                "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            },
        ]

        vacancies = Vacancy.cast_to_object_list(data_list)

        assert len(vacancies) == 2
        assert vacancies[0]._name == "Python Developer"
        assert vacancies[1]._name == "Java Developer"
        assert isinstance(vacancies[0], Vacancy)
        assert isinstance(vacancies[1], Vacancy)
