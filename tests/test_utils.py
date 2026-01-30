import pytest
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies
)
from src.vacancy import Vacancy


class TestUtils:
    """Тесты для вспомогательных функций"""

    @pytest.fixture
    def sample_vacancies(self):
        """Фикстура с тестовыми вакансиями"""
        return [
            Vacancy(
                _id="1",
                _name="Python Developer",
                _url="url1",
                _salary_from=100000,
                _salary_to=150000,
                _description="Нужно знать Django и Flask",
                _experience="Middle"
            ),
            Vacancy(
                _id="2",
                _name="Java Developer",
                _url="url2",
                _salary_from=80000,
                _salary_to=120000,
                _description="Требуется Java Spring",
                _experience="Senior"
            ),
            Vacancy(
                _id="3",
                _name="Python Data Scientist",
                _url="url3",
                _salary_from=150000,
                _salary_to=200000,
                _description="Python, pandas, numpy",
                _experience="Senior"
            ),
        ]

    def test_filter_vacancies(self, sample_vacancies):
        """Тест фильтрации по ключевым словам"""
        # Фильтр по "Python"
        filtered = filter_vacancies(sample_vacancies, ["Python"])
        assert len(filtered) == 2
        assert all("Python" in vacancy._name for vacancy in filtered)

        # Фильтр по "Senior"
        filtered = filter_vacancies(sample_vacancies, ["Senior"])
        assert len(filtered) == 2

        # Фильтр по нескольким словам
        filtered = filter_vacancies(sample_vacancies, ["Python", "Senior"])
        assert len(filtered) == 1
        assert filtered[0]._name == "Python Data Scientist"

        # Без фильтра
        filtered = filter_vacancies(sample_vacancies, [])
        assert len(filtered) == 3

    def test_get_vacancies_by_salary(self, sample_vacancies):
        """Тест фильтрации по зарплате"""
        # Диапазон 100000-150000
        filtered = get_vacancies_by_salary(sample_vacancies, "100000-150000")
        assert len(filtered) == 1
        assert filtered[0]._name == "Python Developer"

        # Диапазон от 120000
        filtered = get_vacancies_by_salary(sample_vacancies, "120000")
        assert len(filtered) == 2

        # Диапазон 80000-120000
        filtered = get_vacancies_by_salary(sample_vacancies, "80000-120000")
        assert len(filtered) == 2

        # Некорректный диапазон
        filtered = get_vacancies_by_salary(sample_vacancies, "invalid")
        assert len(filtered) == 3  # Возвращает все при ошибке

        # Пустой диапазон
        filtered = get_vacancies_by_salary(sample_vacancies, "")
        assert len(filtered) == 3

    def test_sort_vacancies(self, sample_vacancies):
        """Тест сортировки вакансий"""
        sorted_vacancies = sort_vacancies(sample_vacancies)

        # Проверяем что отсортировано по убыванию зарплаты
        assert sorted_vacancies[0].avg_salary >= sorted_vacancies[1].avg_salary
        assert sorted_vacancies[1].avg_salary >= sorted_vacancies[2].avg_salary

        # Конкретные значения
        assert sorted_vacancies[0]._name == "Python Data Scientist"  # 175k
        assert sorted_vacancies[1]._name == "Python Developer"  # 125k
        assert sorted_vacancies[2]._name == "Java Developer"  # 100k

    def test_get_top_vacancies(self, sample_vacancies):
        """Тест получения топ N вакансий"""
        sorted_vacancies = sort_vacancies(sample_vacancies)

        # Топ 2
        top_2 = get_top_vacancies(sorted_vacancies, 2)
        assert len(top_2) == 2
        assert top_2[0]._name == "Python Data Scientist"
        assert top_2[1]._name == "Python Developer"

        # Топ 10 (больше чем есть)
        top_10 = get_top_vacancies(sorted_vacancies, 10)
        assert len(top_10) == 3

        # Топ 0
        top_0 = get_top_vacancies(sorted_vacancies, 0)
        assert len(top_0) == 0

    def test_print_vacancies(self, sample_vacancies, capsys):
        """Тест вывода вакансий"""
        print_vacancies(sample_vacancies)

        captured = capsys.readouterr()
        output = captured.out

        # Проверяем что вывод содержит нужную информацию
        assert "Python Developer" in output
        assert "Java Developer" in output
        assert "Python Data Scientist" in output
        assert "Зарплата:" in output
        assert "Ссылка:" in output

        # Пустой список
        print_vacancies([])
        captured = capsys.readouterr()
        assert "Вакансии не найдены" in captured.out
