"""
Тесты для основного модуля main.py
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from io import StringIO

# Импортируем весь модуль
import src.main


class TestPrintFunctions:
    """Тесты для функций вывода"""

    def test_show_all_vacancies_empty(self):
        """Тест вывода пустого списка вакансий"""
        mock_db = Mock()
        mock_db.get_all_vacancies.return_value = []

        with patch('builtins.print') as mock_print:
            src.main.show_all_vacancies(mock_db)
            # Должен вызвать print хотя бы раз
            assert mock_print.called

    def test_show_all_vacancies_with_data(self):
        """Тест вывода вакансий с данными"""
        mock_db = Mock()
        mock_db.get_all_vacancies.return_value = [
            {
                'company_name': 'Yandex',
                'vacancy_name': 'Python Developer',
                'salary_from': 100000,
                'salary_to': 150000,
                'salary_currency': 'RUR',
                'url': 'https://hh.ru/vacancy/1'
            }
        ]

        with patch('builtins.print') as mock_print:
            src.main.show_all_vacancies(mock_db)
            assert mock_print.call_count >= 5

    def test_show_all_vacancies_without_salary(self):
        """Тест вывода вакансий без зарплаты"""
        mock_db = Mock()
        mock_db.get_all_vacancies.return_value = [
            {
                'company_name': 'Yandex',
                'vacancy_name': 'Python Developer',
                'salary_from': None,
                'salary_to': None,
                'salary_currency': None,
                'url': 'https://hh.ru/vacancy/1'
            }
        ]

        with patch('builtins.print') as mock_print:
            src.main.show_all_vacancies(mock_db)
            # Проверяем что функция не падает
            assert mock_print.called

    def test_show_all_vacancies_only_from(self):
        """Тест вывода вакансий только с salary_from"""
        mock_db = Mock()
        mock_db.get_all_vacancies.return_value = [
            {
                'company_name': 'Yandex',
                'vacancy_name': 'Python Developer',
                'salary_from': 100000,
                'salary_to': None,
                'salary_currency': 'RUR',
                'url': 'https://hh.ru/vacancy/1'
            }
        ]

        with patch('builtins.print') as mock_print:
            src.main.show_all_vacancies(mock_db)
            assert mock_print.called

    def test_show_all_vacancies_only_to(self):
        """Тест вывода вакансий только с salary_to"""
        mock_db = Mock()
        mock_db.get_all_vacancies.return_value = [
            {
                'company_name': 'Yandex',
                'vacancy_name': 'Python Developer',
                'salary_from': None,
                'salary_to': 150000,
                'salary_currency': 'RUR',
                'url': 'https://hh.ru/vacancy/1'
            }
        ]

        with patch('builtins.print') as mock_print:
            src.main.show_all_vacancies(mock_db)
            assert mock_print.called

    def test_show_companies_stats_empty(self):
        """Тест вывода пустой статистики компаний"""
        mock_db = Mock()
        mock_db.get_companies_and_vacancies_count.return_value = []

        with patch('builtins.print') as mock_print:
            src.main.show_companies_stats(mock_db)
            # Проверяем что функция не падает
            assert mock_print.called

    def test_show_companies_stats_with_data(self):
        """Тест вывода статистики компаний"""
        mock_db = Mock()
        mock_db.get_companies_and_vacancies_count.return_value = [
            {'company_name': 'Yandex', 'vacancies_count': 10},
            {'company_name': 'Sber', 'vacancies_count': 5}
        ]

        with patch('builtins.print') as mock_print:
            src.main.show_companies_stats(mock_db)
            assert mock_print.call_count >= 3

    def test_show_average_salary(self):
        """Тест вывода средней зарплаты"""
        mock_db = Mock()
        mock_db.get_avg_salary.return_value = 150000

        with patch('builtins.print') as mock_print:
            src.main.show_average_salary(mock_db)
            assert mock_print.called

    def test_show_average_salary_none(self):
        """Тест вывода средней зарплаты когда нет данных"""
        mock_db = Mock()
        mock_db.get_avg_salary.return_value = None

        with patch('builtins.print') as mock_print:
            src.main.show_average_salary(mock_db)
            assert mock_print.called

    def test_show_higher_salary_vacancies(self):
        """Тест вывода вакансий выше средней"""
        mock_db = Mock()
        mock_db.get_vacancies_with_higher_salary.return_value = []

        with patch('builtins.print') as mock_print:
            src.main.show_higher_salary_vacancies(mock_db)
            assert mock_print.called

    def test_search_vacancies_by_keyword(self):
        """Тест поиска по ключевому слову"""
        mock_db = Mock()
        mock_db.get_vacancies_with_keyword.return_value = []

        with patch('builtins.input', return_value='python'):
            with patch('builtins.print') as mock_print:
                src.main.search_vacancies_by_keyword(mock_db)
                assert mock_print.called


class TestUserInteraction:
    """Тесты для функции user_interaction"""

    @patch('src.main.input')
    @patch('src.main.print')
    def test_exit_program(self, mock_print, mock_input):
        """Тест выхода из программы"""
        mock_input.side_effect = ['8']

        try:
            src.main.user_interaction()
        except Exception:
            pass

        assert mock_print.called

    @patch('src.main.input')
    @patch('src.main.DBCreator')
    def test_create_tables_option(self, mock_db_creator, mock_input):
        """Тест создания таблиц"""
        mock_input.side_effect = ['1', '8']

        try:
            src.main.user_interaction()
        except Exception:
            pass

        mock_db_creator.create_tables.assert_called_once()

    @patch('src.main.input')
    @patch('src.main.load_companies_vacancies')
    def test_load_data_option(self, mock_load, mock_input):
        """Тест загрузки данных"""
        mock_input.side_effect = ['2', '8']

        try:
            src.main.user_interaction()
        except Exception:
            pass

        mock_load.assert_called_once()

    @patch('src.main.input')
    @patch('src.main.DBManager')
    @patch('src.main.show_companies_stats')
    def test_companies_stats_option(self, mock_show_stats, mock_db_manager, mock_input):
        """Тест получения статистики компаний"""
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance

        mock_input.side_effect = ['2', '3', '8']

        with patch('src.main.load_companies_vacancies'):
            try:
                src.main.user_interaction()
            except Exception:
                pass

            mock_show_stats.assert_called_once()

    @patch('src.main.input')
    @patch('src.main.DBManager')
    @patch('src.main.show_all_vacancies')
    def test_all_vacancies_option(self, mock_show_vac, mock_db_manager, mock_input):
        """Тест вывода всех вакансий"""
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance

        mock_input.side_effect = ['2', '4', '8']

        with patch('src.main.load_companies_vacancies'):
            try:
                src.main.user_interaction()
            except Exception:
                pass

            mock_show_vac.assert_called_once()

    @patch('src.main.input')
    @patch('src.main.DBManager')
    @patch('src.main.show_average_salary')
    def test_avg_salary_option(self, mock_show_avg, mock_db_manager, mock_input):
        """Тест средней зарплаты"""
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance

        mock_input.side_effect = ['2', '5', '8']

        with patch('src.main.load_companies_vacancies'):
            try:
                src.main.user_interaction()
            except Exception:
                pass

            mock_show_avg.assert_called_once()

    @patch('src.main.input')
    @patch('src.main.DBManager')
    @patch('src.main.show_higher_salary_vacancies')
    def test_higher_salary_option(self, mock_show_higher, mock_db_manager, mock_input):
        """Тест вакансий выше средней"""
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance

        mock_input.side_effect = ['2', '6', '8']

        with patch('src.main.load_companies_vacancies'):
            try:
                src.main.user_interaction()
            except Exception:
                pass

            mock_show_higher.assert_called_once()

    @patch('src.main.input')
    @patch('src.main.DBManager')
    @patch('src.main.search_vacancies_by_keyword')
    def test_keyword_search_option(self, mock_search, mock_db_manager, mock_input):
        """Тест поиска по ключевому слову"""
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance

        mock_input.side_effect = ['2', '7', 'python', '8']

        with patch('src.main.load_companies_vacancies'):
            try:
                src.main.user_interaction()
            except Exception:
                pass

            mock_search.assert_called_once()

    @patch('src.main.input')
    def test_invalid_choice(self, mock_input):
        """Тест некорректного выбора"""
        mock_input.side_effect = ['99', '8']

        with patch('builtins.print') as mock_print:
            try:
                src.main.user_interaction()
            except Exception:
                pass

            # Проверяем что сообщение об ошибке выводилось
            found = False
            for call in mock_print.call_args_list:
                if 'Неверный выбор' in str(call):
                    found = True
                    break
            assert found


class TestMainModule:
    """Тесты для модуля main"""

    def test_main_import(self):
        """Тест импорта main"""
        assert src.main is not None

    def test_main_has_functions(self):
        """Тест что в main есть все функции"""
        assert hasattr(src.main, 'user_interaction')
        assert hasattr(src.main, 'show_all_vacancies')
        assert hasattr(src.main, 'show_companies_stats')
        assert hasattr(src.main, 'show_average_salary')
        assert hasattr(src.main, 'show_higher_salary_vacancies')
        assert hasattr(src.main, 'search_vacancies_by_keyword')
        assert hasattr(src.main, 'handle_database_creation')
        assert hasattr(src.main, 'handle_data_loading')
        assert callable(src.main.user_interaction)
        assert callable(src.main.show_all_vacancies)
        assert callable(src.main.show_companies_stats)
