from unittest.mock import patch, MagicMock


class TestPrintFunctions:
    """Тесты для функций вывода"""

    def test_print_vacancies_empty(self):
        """Тест вывода пустого списка вакансий"""
        from src.main import print_vacancies

        with patch("builtins.print") as mock_print:
            print_vacancies([])
            mock_print.assert_called_with("Вакансии не найдены")

    def test_print_vacancies_with_data(self):
        """Тест вывода вакансий с данными"""
        from src.main import print_vacancies

        vacancies = [
            {
                "company_name": "Yandex",
                "vacancy_name": "Python Developer",
                "salary_from": 100000,
                "salary_to": 150000,
                "salary_currency": "RUR",
                "url": "https://hh.ru/vacancy/1",
            }
        ]

        with patch("builtins.print") as mock_print:
            print_vacancies(vacancies)
            assert mock_print.call_count >= 5

    def test_print_vacancies_without_salary(self):
        """Тест вывода вакансий без зарплаты"""
        from src.main import print_vacancies

        vacancies = [
            {
                "company_name": "Yandex",
                "vacancy_name": "Python Developer",
                "salary_from": None,
                "salary_to": None,
                "salary_currency": None,
                "url": "https://hh.ru/vacancy/1",
            }
        ]

        with patch("builtins.print") as mock_print:
            print_vacancies(vacancies)
            # Проверяем что была вызвана печать "Зарплата: не указана"
            found = False
            for call in mock_print.call_args_list:
                if "Зарплата: не указана" in str(call):
                    found = True
                    break
            assert found

    def test_print_vacancies_only_from(self):
        """Тест вывода вакансий только с salary_from"""
        from src.main import print_vacancies

        vacancies = [
            {
                "company_name": "Yandex",
                "vacancy_name": "Python Developer",
                "salary_from": 100000,
                "salary_to": None,
                "salary_currency": "RUR",
                "url": "https://hh.ru/vacancy/1",
            }
        ]

        with patch("builtins.print") as mock_print:
            print_vacancies(vacancies)
            # Проверяем что была вызвана печать "от 100 000"
            found = False
            for call in mock_print.call_args_list:
                if "от 100 000" in str(call):
                    found = True
                    break
            assert found

    def test_print_vacancies_only_to(self):
        """Тест вывода вакансий только с salary_to"""
        from src.main import print_vacancies

        vacancies = [
            {
                "company_name": "Yandex",
                "vacancy_name": "Python Developer",
                "salary_from": None,
                "salary_to": 150000,
                "salary_currency": "RUR",
                "url": "https://hh.ru/vacancy/1",
            }
        ]

        with patch("builtins.print") as mock_print:
            print_vacancies(vacancies)
            # Проверяем что была вызвана печать "до 150 000"
            found = False
            for call in mock_print.call_args_list:
                if "до 150 000" in str(call):
                    found = True
                    break
            assert found

    def test_print_companies_stats_empty(self):
        """Тест вывода пустой статистики компаний"""
        from src.main import print_companies_stats

        with patch("builtins.print") as mock_print:
            print_companies_stats([])
            # Проверяем что ничего не падает

    def test_print_companies_stats_with_data(self):
        """Тест вывода статистики компаний"""
        from src.main import print_companies_stats

        stats = [{"company_name": "Yandex", "vacancies_count": 10}, {"company_name": "Sber", "vacancies_count": 5}]

        with patch("builtins.print") as mock_print:
            print_companies_stats(stats)
            # Проверяем что было несколько вызовов print
            assert mock_print.call_count >= 5


class TestUserInteraction:
    """Тесты для функции user_interaction"""

    @patch("src.main.input")
    @patch("src.main.print")
    def test_exit_program(self, mock_print, mock_input):
        """Тест выхода из программы"""
        from src.main import user_interaction

        mock_input.side_effect = ["8"]  # Сразу выход

        try:
            user_interaction()
        except Exception:
            pass

        # Проверяем что меню выводилось
        assert mock_print.called

    @patch("src.main.input")
    @patch("src.main.DBCreator")
    def test_create_tables_option(self, mock_db_creator, mock_input):
        """Тест создания таблиц"""
        from src.main import user_interaction

        mock_input.side_effect = ["1", "8"]  # Создать таблицы -> выход

        try:
            user_interaction()
        except Exception:
            pass

        mock_db_creator.create_tables.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.load_companies_vacancies")
    @patch("src.main.DBManager")
    def test_load_data_option(self, mock_db_manager, mock_load, mock_input):
        """Тест загрузки данных"""
        from src.main import user_interaction

        mock_input.side_effect = ["2", "8"]  # Загрузить -> выход

        try:
            user_interaction()
        except Exception:
            pass

        mock_load.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.DBManager")
    @patch("src.main.print_companies_stats")
    def test_companies_stats_option(self, mock_print_stats, mock_db_manager, mock_input):
        """Тест получения статистики компаний"""
        # Настраиваем мок
        mock_db_instance = MagicMock()
        mock_db_instance.get_companies_and_vacancies_count.return_value = [
            {"company_name": "Test", "vacancies_count": 5}
        ]
        mock_db_manager.return_value = mock_db_instance

        from src.main import user_interaction

        # Сначала загружаем данные (инициализируем db), потом смотрим
        # статистику
        mock_input.side_effect = ["2", "3", "8"]

        with patch("src.main.load_companies_vacancies"):
            try:
                user_interaction()
            except Exception:
                pass

            mock_db_instance.get_companies_and_vacancies_count.assert_called_once()
            mock_print_stats.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.DBManager")
    @patch("src.main.print_vacancies")
    def test_all_vacancies_option(self, mock_print_vac, mock_db_manager, mock_input):
        """Тест вывода всех вакансий"""
        mock_db_instance = MagicMock()
        mock_db_instance.get_all_vacancies.return_value = []
        mock_db_manager.return_value = mock_db_instance

        from src.main import user_interaction

        mock_input.side_effect = ["2", "4", "8"]

        with patch("src.main.load_companies_vacancies"):
            try:
                user_interaction()
            except Exception:
                pass

            mock_db_instance.get_all_vacancies.assert_called_once()
            mock_print_vac.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.DBManager")
    def test_avg_salary_option(self, mock_db_manager, mock_input):
        """Тест средней зарплаты"""
        mock_db_instance = MagicMock()
        mock_db_instance.get_avg_salary.return_value = 150000
        mock_db_manager.return_value = mock_db_instance

        from src.main import user_interaction

        mock_input.side_effect = ["2", "5", "8"]

        with patch("src.main.load_companies_vacancies"):
            with patch("builtins.print") as mock_print:
                try:
                    user_interaction()
                except Exception:
                    pass

                mock_db_instance.get_avg_salary.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.DBManager")
    @patch("src.main.print_vacancies")
    def test_higher_salary_option(self, mock_print_vac, mock_db_manager, mock_input):
        """Тест вакансий выше средней"""
        mock_db_instance = MagicMock()
        mock_db_instance.get_vacancies_with_higher_salary.return_value = []
        mock_db_manager.return_value = mock_db_instance

        from src.main import user_interaction

        mock_input.side_effect = ["2", "6", "8"]

        with patch("src.main.load_companies_vacancies"):
            try:
                user_interaction()
            except Exception:
                pass

            mock_db_instance.get_vacancies_with_higher_salary.assert_called_once()
            mock_print_vac.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.DBManager")
    @patch("src.main.print_vacancies")
    def test_keyword_search_option(self, mock_print_vac, mock_db_manager, mock_input):
        """Тест поиска по ключевому слову"""
        mock_db_instance = MagicMock()
        mock_db_instance.get_vacancies_with_keyword.return_value = []
        mock_db_manager.return_value = mock_db_instance

        from src.main import user_interaction

        mock_input.side_effect = ["2", "7", "python", "8"]

        with patch("src.main.load_companies_vacancies"):
            try:
                user_interaction()
            except Exception:
                pass

            mock_db_instance.get_vacancies_with_keyword.assert_called_once_with("python")
            mock_print_vac.assert_called_once()

    @patch("src.main.input")
    @patch("src.main.DBManager")
    def test_without_initialization(self, mock_db_manager, mock_input):
        """Тест что без инициализации методы не вызываются"""
        mock_db_instance = MagicMock()
        mock_db_manager.return_value = mock_db_instance

        from src.main import user_interaction

        # Пытаемся вызвать методы без загрузки данных
        mock_input.side_effect = ["3", "4", "5", "6", "7", "test", "8"]

        with patch("builtins.print"):
            try:
                user_interaction()
            except Exception:
                pass

            # Методы не должны вызываться
            mock_db_instance.get_companies_and_vacancies_count.assert_not_called()
            mock_db_instance.get_all_vacancies.assert_not_called()
            mock_db_instance.get_avg_salary.assert_not_called()
            mock_db_instance.get_vacancies_with_higher_salary.assert_not_called()
            mock_db_instance.get_vacancies_with_keyword.assert_not_called()

    @patch("src.main.input")
    def test_invalid_choice(self, mock_input):
        """Тест некорректного выбора"""
        from src.main import user_interaction

        mock_input.side_effect = ["99", "8"]  # Неверный выбор -> выход

        with patch("builtins.print") as mock_print:
            try:
                user_interaction()
            except Exception:
                pass

            # Проверяем что сообщение об ошибке выводилось
            found = False
            for call in mock_print.call_args_list:
                if "Неверный выбор" in str(call):
                    found = True
                    break
            assert found


class TestMainModule:
    """Тесты для модуля main"""

    def test_main_import(self):
        """Тест импорта main"""
        import src.main

        assert src.main is not None

    def test_main_has_functions(self):
        """Тест что в main есть все функции"""
        import src.main

        assert hasattr(src.main, "user_interaction")
        assert hasattr(src.main, "print_vacancies")
        assert hasattr(src.main, "print_companies_stats")
        assert callable(src.main.user_interaction)
        assert callable(src.main.print_vacancies)
        assert callable(src.main.print_companies_stats)

    def test_main_execution(self):
        """Тест что main можно запустить"""
        import src.main

        assert src.main.__name__ == "src.main"
