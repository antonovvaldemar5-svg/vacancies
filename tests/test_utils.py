"""
Тесты для утилитных функций работы с вакансиями.
"""

from src.utils import filter_vacancies, get_vacancies_by_salary, sort_vacancies, get_top_vacancies, print_vacancies
from src.vacancy import Vacancy


class TestUtils:
    """Тесты для утилитных функций"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.vacancies = [
            Vacancy(
                _id="1",
                _name="Python Developer",
                _url="url1",
                _salary_from=100000,
                _salary_to=150000,
                _description="Разработка на Python и Django",
                _experience="От 1 года до 3 лет",
                _employer="Company A",
            ),
            Vacancy(
                _id="2",
                _name="Java Developer",
                _url="url2",
                _salary_from=120000,
                _salary_to=180000,
                _description="Разработка на Java Spring",
                _experience="От 3 до 6 лет",
                _employer="Company B",
            ),
            Vacancy(
                _id="3",
                _name="Python Senior",
                _url="url3",
                _salary_from=200000,
                _salary_to=300000,
                _description="Python разработка архитектуры",
                _experience="Более 6 лет",
                _employer="Company C",
            ),
            Vacancy(
                _id="4",
                _name="JavaScript Developer",
                _url="url4",
                _salary_from=80000,
                _salary_to=120000,
                _description="Frontend разработка на React",
                _experience="Нет опыта",
                _employer="Company D",
            ),
        ]

    def test_filter_vacancies_with_keywords(self):
        """Тест фильтрации по ключевым словам"""
        # Фильтр по "Python"
        filtered = filter_vacancies(self.vacancies, ["Python"])
        assert len(filtered) == 2
        assert all("Python" in vacancy._name for vacancy in filtered)

        # Фильтр по "Senior"
        filtered = filter_vacancies(self.vacancies, ["Senior"])
        assert len(filtered) == 1
        assert filtered[0]._name == "Python Senior"

        # Фильтр по нескольким словам
        filtered = filter_vacancies(self.vacancies, ["Python", "Senior"])
        assert len(filtered) == 2

        # Фильтр по компании
        filtered = filter_vacancies(self.vacancies, ["Company C"])
        assert len(filtered) == 1
        assert filtered[0]._employer == "Company C"

    def test_filter_vacancies_case_insensitive(self):
        """Тест регистронезависимой фильтрации"""
        filtered = filter_vacancies(self.vacancies, ["python"])
        assert len(filtered) == 2

        filtered = filter_vacancies(self.vacancies, ["PYTHON"])
        assert len(filtered) == 2

    def test_filter_vacancies_no_filter_words(self):
        """Тест фильтрации без ключевых слов"""
        filtered = filter_vacancies(self.vacancies, [])
        assert len(filtered) == len(self.vacancies)

    def test_filter_vacancies_no_matches(self):
        """Тест когда нет совпадений"""
        filtered = filter_vacancies(self.vacancies, ["C++"])
        assert len(filtered) == 0

    def test_get_vacancies_by_salary_range(self):
        """Тест фильтрации по диапазону зарплат"""
        # Диапазон 100000-200000
        filtered = get_vacancies_by_salary(self.vacancies, "100000-200000")
        # Все вакансии пересекаются с этим диапазоном
        assert len(filtered) == 4

        # Более узкий диапазон
        filtered = get_vacancies_by_salary(self.vacancies, "150000-250000")
        # JavaScript Developer: 80k-120k (НЕТ) ✗
        # Остальные пересекаются: ✓
        assert len(filtered) == 3

    def test_get_vacancies_by_salary_edge_cases(self):
        """Тест крайних случаев фильтрации по зарплате"""
        # Пустой диапазон
        filtered = get_vacancies_by_salary(self.vacancies, "")
        assert len(filtered) == 4

        # Некорректный формат
        filtered = get_vacancies_by_salary(self.vacancies, "не число")
        assert len(filtered) == 4

        # Очень низкая зарплата (0-50000)
        filtered = get_vacancies_by_salary(self.vacancies, "0-50000")
        # Ни одна вакансия не пересекается с 0-50k
        assert len(filtered) == 0

        # Очень высокая зарплата
        filtered = get_vacancies_by_salary(self.vacancies, "500000-1000000")
        assert len(filtered) == 0

        # Только минимальная зарплата (150000)
        filtered = get_vacancies_by_salary(self.vacancies, "150000")
        # Все вакансии имеют максимальную зарплату >= 150k
        # JavaScript: 120k >= 150k? ДА (120k >= 150k? НЕТ! Исправляем)
        # Python Dev: 150k >= 150k? ДА
        # Java: 180k >= 150k? ДА
        # Python Senior: 300k >= 150k? ДА
        # Только JavaScript не подходит (120k < 150k)
        assert len(filtered) == 3  # Исправлено с 4 на 3!

        # Только максимальная зарплата (до 150000)
        filtered = get_vacancies_by_salary(self.vacancies, "0-150000")
        # JavaScript Developer: 80k-120k ✓ (входит полностью)
        # Python Developer: 100k-150k ✓ (входит полностью)
        # Java Developer: 120k-180k ✓ (пересекается 120k-150k)
        # Python Senior: 200k-300k ✗ (не пересекается)
        assert len(filtered) == 3

    def test_get_vacancies_by_salary_single_value(self):
        """Тест фильтрации по одному числу (от этого числа)"""
        filtered = get_vacancies_by_salary(self.vacancies, "120000")
        # JavaScript: 120k >= 120k? ДА
        # Python Dev: 150k >= 120k? ДА
        # Java: 180k >= 120k? ДА
        # Python Senior: 300k >= 120k? ДА
        assert len(filtered) == 4

        filtered = get_vacancies_by_salary(self.vacancies, "180000")
        # JavaScript: 120k >= 180k? НЕТ
        # Python Dev: 150k >= 180k? НЕТ
        # Java: 180k >= 180k? ДА
        # Python Senior: 300k >= 180k? ДА
        assert len(filtered) == 2

    def test_get_vacancies_by_salary_with_spaces(self):
        """Тест фильтрации с пробелами в диапазоне"""
        filtered = get_vacancies_by_salary(self.vacancies, "100000 - 200000")
        assert len(filtered) == 4

        filtered = get_vacancies_by_salary(self.vacancies, " 150000 ")
        # JavaScript: 120k >= 150k? НЕТ
        # Python Dev: 150k >= 150k? ДА
        # Java: 180k >= 150k? ДА
        # Python Senior: 300k >= 150k? ДА
        assert len(filtered) == 3  # Исправлено с 4 на 3!

    def test_sort_vacancies(self):
        """Тест сортировки вакансий"""
        sorted_list = sort_vacancies(self.vacancies)

        # Проверяем что отсортировано по убыванию зарплаты
        assert sorted_list[0]._name == "Python Senior"  # 250k avg
        assert sorted_list[1]._name == "Java Developer"  # 150k avg
        assert sorted_list[2]._name == "Python Developer"  # 125k avg
        assert sorted_list[3]._name == "JavaScript Developer"  # 100k avg

    def test_get_top_vacancies(self):
        """Тест получения топ N вакансий"""
        sorted_vacancies = sort_vacancies(self.vacancies)

        top_2 = get_top_vacancies(sorted_vacancies, 2)
        assert len(top_2) == 2
        assert top_2[0]._name == "Python Senior"
        assert top_2[1]._name == "Java Developer"

        top_10 = get_top_vacancies(sorted_vacancies, 10)
        assert len(top_10) == 4  # Все вакансии, так как их меньше 10

    def test_get_top_vacancies_zero_or_negative(self):
        """Тест с нулевым или отрицательным N"""
        top_0 = get_top_vacancies(self.vacancies, 0)
        assert len(top_0) == 0

        top_negative = get_top_vacancies(self.vacancies, -5)
        assert len(top_negative) == 0

    def test_print_vacancies_empty_list(self, capsys):
        """Тест вывода пустого списка вакансий"""
        print_vacancies([])
        captured = capsys.readouterr()
        assert "Вакансии не найдены" in captured.out

    def test_print_vacancies_with_data(self, capsys):
        """Тест вывода списка вакансий"""
        print_vacancies(self.vacancies[:1])
        captured = capsys.readouterr()

        assert "Вакансия #1" in captured.out
        assert "Python Developer" in captured.out
        assert "от 100 000" in captured.out
        assert "до 150 000" in captured.out


class TestUtilsAdvanced:
    """Дополнительные тесты утилит"""

    def test_filter_vacancies_with_partial_words(self):
        """Тест фильтрации по части слова"""
        vacancies = [
            Vacancy(_id="1", _name="Django разработчик", _url="url", _description="Python Django"),
            Vacancy(_id="2", _name="Python разработчик", _url="url", _description="Django Flask"),
        ]

        filtered = filter_vacancies(vacancies, ["jango"])
        # Оба содержат "jango" в "Django"
        assert len(filtered) == 2

        filtered = filter_vacancies(vacancies, ["Pyth"])
        assert len(filtered) == 2

    def test_get_vacancies_by_salary_no_salary_vacancies(self):
        """Тест фильтрации при наличии вакансий без зарплаты"""
        vacancies = [
            Vacancy(_id="1", _name="With Salary", _url="url", _salary_from=100000, _salary_to=150000),
            Vacancy(_id="2", _name="No Salary", _url="url"),  # Без зарплаты
            Vacancy(_id="3", _name="Another With Salary", _url="url", _salary_from=200000, _salary_to=250000),
        ]

        # Вакансии без зарплаты не должны попадать в результаты фильтрации
        filtered = get_vacancies_by_salary(vacancies, "120000")
        assert len(filtered) == 2
        assert all(v._name != "No Salary" for v in filtered)

        # При пустом диапазоне все возвращаются
        filtered = get_vacancies_by_salary(vacancies, "")
        assert len(filtered) == 3

    def test_get_vacancies_by_salary_only_from_or_to(self):
        """Тест фильтрации при вакансиях с только одной границей зарплаты"""
        vacancies = [
            Vacancy(_id="1", _name="Only From", _url="url", _salary_from=100000),
            # Только от
            Vacancy(_id="2", _name="Only To", _url="url", _salary_to=150000),
            # Только до
            Vacancy(_id="3", _name="Both", _url="url", _salary_from=120000, _salary_to=180000),
        ]

        # Фильтр 80000: все подходят
        filtered = get_vacancies_by_salary(vacancies, "80000")
        assert len(filtered) == 3

        # Фильтр 160000:
        # Only From: 100k (max=100k) >= 160k? НЕТ
        # Only To: 150k (min=0, max=150k) >= 160k? НЕТ
        # Both: 180k (max) >= 160k? ДА
        filtered = get_vacancies_by_salary(vacancies, "160000")
        assert len(filtered) == 1

        # Фильтр 0-130000:
        # Only From: 100k (min) <= 130k? ДА, 100k (max) >= 0? ДА ✓
        # Only To: 0 (min) <= 130k? ДА, 150k (max) >= 0? ДА ✓
        # Both: 120k (min) <= 130k? ДА, 180k (max) >= 0? ДА ✓
        filtered = get_vacancies_by_salary(vacancies, "0-130000")
        assert len(filtered) == 3
