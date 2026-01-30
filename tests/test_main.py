import pytest
from unittest.mock import Mock, patch, MagicMock
import builtins
from io import StringIO
import sys
import json
import os
from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_handlers import JSONSaver


class TestMain:
    """Тесты для основного модуля (user_interaction)"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.mock_api = Mock(spec=HeadHunterAPI)
        self.mock_saver = Mock(spec=JSONSaver)

    @patch('builtins.input')
    @patch('builtins.print')
    @patch('src.api.HeadHunterAPI')
    @patch('src.file_handlers.JSONSaver')
    def test_user_interaction_search_vacancies(self, mock_saver, mock_api, mock_print, mock_input):
        """Тест поиска и сохранения вакансий"""
        from src.main import user_interaction

        # Настраиваем моки
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        mock_saver_instance = Mock()
        mock_saver.return_value = mock_saver_instance

        # Тестовые данные вакансий
        test_vacancies = [
            {
                "id": "1",
                "name": "Python Developer",
                "url": "https://hh.ru/vacancy/1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Test",
                "experience": "1-3 years",
                "employer": "Test Company",
                "published_at": "2024-01-01"
            }
        ]

        mock_api_instance.get_vacancies.return_value = test_vacancies

        # Симулируем ввод пользователя: поиск -> показать первые 5 -> выход
        mock_input.side_effect = [
            '1',  # Выбор поиска
            'Python',  # Поисковый запрос
            '10',  # Количество вакансий
            'n',  # Не показывать первые 5
            '8'  # Выход
        ]

        try:
            user_interaction()
        except SystemExit:
            pass

        # Проверяем что API вызывалось
        mock_api_instance.get_vacancies.assert_called_once_with('Python', per_page=10)

        # Проверяем что савер вызывался для добавления
        assert mock_saver_instance.add_vacancy.called

    @patch('builtins.input')
    @patch('builtins.print')
    def test_top_n_vacancies_flow(self, mock_print, mock_input):
        """Тест получения топ N вакансий"""
        # Импортируем здесь чтобы избежать проблем с моками
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Настраиваем моки
                test_data = [
                    {
                        "id": "1",
                        "name": "Python",
                        "salary_from": 100000,
                        "salary_to": 150000
                    },
                    {
                        "id": "2",
                        "name": "Java",
                        "salary_from": 120000,
                        "salary_to": 180000
                    }
                ]

                self.mock_saver.get_vacancies.return_value = test_data

                # Симулируем ввод: топ N -> выход
                mock_input.side_effect = [
                    '2',  # Топ N вакансий
                    '3',  # 3 вакансии
                    '8'  # Выход
                ]

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что получали вакансии из савера
                self.mock_saver.get_vacancies.assert_called_once()

    @patch('builtins.input')
    @patch('sys.stdout', new_callable=StringIO)
    def test_search_by_keyword_flow(self, mock_stdout, mock_input):
        """Тест поиска по ключевому слову"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction
                from src.vacancy import Vacancy

                # Создаем тестовые объекты Vacancy
                vacancy1 = Vacancy(
                    _id="1",
                    _name="Python Developer",
                    _url="url1",
                    _description="Python and Django development",
                    _salary_from=100000,
                    _salary_to=150000
                )

                vacancy2 = Vacancy(
                    _id="2",
                    _name="Java Developer",
                    _url="url2",
                    _description="Java Spring development",
                    _salary_from=120000,
                    _salary_to=180000
                )

                # Мокаем Vacancy.cast_to_object_list
                with patch('src.main.Vacancy.cast_to_object_list', return_value=[vacancy1, vacancy2]):
                    # Мокаем filter_vacancies чтобы возвращать только Python вакансии
                    with patch('src.main.filter_vacancies', return_value=[vacancy1]):
                        # Симулируем ввод
                        mock_input.side_effect = [
                            '3',  # Поиск по ключевому слову
                            'python',  # Ключевое слово
                            '8'  # Выход
                        ]

                        try:
                            user_interaction()
                        except SystemExit:
                            pass

                        # Проверяем вывод
                        output = mock_stdout.getvalue()
                        assert "Найдено 1 вакансий" in output or "вакансий с ключевым словом" in output

    @patch('builtins.input')
    def test_salary_range_flow(self, mock_input):
        """Тест поиска по диапазону зарплат"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Симулируем ввод
                mock_input.side_effect = [
                    '4',  # Поиск по зарплате
                    '100000-150000',  # Диапазон
                    '8'  # Выход
                ]

                # Мокаем методы
                self.mock_saver.get_vacancies.return_value = []

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что вызывался get_vacancies
                self.mock_saver.get_vacancies.assert_called_once()

    @patch('builtins.input')
    def test_delete_vacancy_flow(self, mock_input):
        """Тест удаления вакансии"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Симулируем ввод
                mock_input.side_effect = [
                    '6',  # Удаление вакансии
                    '123',  # ID вакансии
                    '8'  # Выход
                ]

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что вызывался delete_vacancy
                self.mock_saver.delete_vacancy.assert_called_once_with('123')

    @patch('builtins.input')
    def test_clear_all_vacancies_flow(self, mock_input):
        """Тест очистки всех вакансий"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Симулируем ввод (с подтверждением)
                mock_input.side_effect = [
                    '7',  # Очистка
                    'y',  # Подтверждение
                    '8'  # Выход
                ]

                # Добавляем метод clear_file в мок
                self.mock_saver.clear_file = Mock()

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что вызывался clear_file
                self.mock_saver.clear_file.assert_called_once()

    @patch('builtins.input')
    def test_show_all_vacancies_flow(self, mock_input):
        """Тест показа всех вакансий"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Тестовые данные
                test_data = [
                    {"id": "1", "name": "Python"},
                    {"id": "2", "name": "Java"}
                ]

                self.mock_saver.get_vacancies.return_value = test_data

                # Симулируем ввод (не показывать все сразу)
                mock_input.side_effect = [
                    '5',  # Показать все
                    'n',  # Не показывать все сразу
                    '',  # Enter для продолжения (первая страница)
                    '',  # Enter для продолжения (вторая страница)
                    '8'  # Выход
                ]

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что получали вакансии
                self.mock_saver.get_vacancies.assert_called_once()

    @patch('builtins.input')
    def test_invalid_choice(self, mock_input):
        """Тест некорректного выбора в меню"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Симулируем ввод: некорректный выбор -> выход
                mock_input.side_effect = [
                    '999',  # Некорректный выбор
                    '8'  # Выход
                ]

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что не вызывались методы API/савера
                assert not self.mock_api.get_vacancies.called
                assert not self.mock_saver.get_vacancies.called

    @patch('builtins.input')
    def test_empty_search_query(self, mock_input):
        """Тест пустого поискового запроса"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Симулируем ввод: поиск с пустым запросом -> выход
                mock_input.side_effect = [
                    '1',  # Поиск
                    '',  # Пустой запрос
                    '8'  # Выход
                ]

                try:
                    user_interaction()
                except SystemExit:
                    pass

                # Проверяем что API не вызывалось
                assert not self.mock_api.get_vacancies.called

    @patch('builtins.input')
    def test_no_saved_vacancies_flow(self, mock_input):
        """Тест когда нет сохраненных вакансий"""
        with patch('src.main.HeadHunterAPI', return_value=self.mock_api):
            with patch('src.main.JSONSaver', return_value=self.mock_saver):
                from src.main import user_interaction

                # Мокаем что нет сохраненных вакансий
                self.mock_saver.get_vacancies.return_value = []

                # Симулируем ввод для разных опций
                test_cases = [
                    ('2', '5'),  # Топ N
                    ('3', 'python'),  # Поиск по ключевому слову
                    ('4', '100000-150000'),  # Поиск по зарплате
                    ('5', '')  # Показать все
                ]

                for menu_choice, user_input in test_cases:
                    mock_input.side_effect = [menu_choice, user_input, '8']

                    try:
                        user_interaction()
                    except SystemExit:
                        pass

                    # Проверяем что get_vacancies вызывался
                    self.mock_saver.get_vacancies.assert_called()
                    self.mock_saver.get_vacancies.reset_mock()

    def test_main_module_execution(self):
        """Тест что модуль main может быть импортирован и запущен"""
        # Просто проверяем что модуль импортируется без ошибок
        from src.main import user_interaction
        assert callable(user_interaction)


class TestMainFunctions:
    """Тесты вспомогательных функций из main"""

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_vacancies_integration(self, mock_stdout):
        """Тест интеграции print_vacancies с реальными объектами"""
        from src.utils import print_vacancies
        from src.vacancy import Vacancy

        vacancy = Vacancy(
            _id="1",
            _name="Test Developer",
            _url="https://test.com",
            _salary_from=100000,
            _salary_to=150000,
            _description="Test description"
        )

        print_vacancies([vacancy])

        output = mock_stdout.getvalue()
        assert "Test Developer" in output
        assert "от 100 000" in output
        assert "до 150 000" in output

    def test_vacancy_cast_integration(self):
        """Тест интеграции cast_to_object_list"""
        from src.vacancy import Vacancy

        test_data = [
            {
                "id": "1",
                "name": "Python",
                "url": "url1",
                "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                "description": "Test",
                "experience": "1-3 years",
                "employer": "Test",
                "published_at": "2024-01-01"
            }
        ]

        vacancies = Vacancy.cast_to_object_list(test_data)

        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0]._name == "Python"
        assert vacancies[0].salary_from == 100000
