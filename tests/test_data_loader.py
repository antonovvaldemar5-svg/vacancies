from unittest.mock import Mock, patch
from src.data_loader import load_companies_vacancies


class TestDataLoader:
    """Тесты для загрузчика данных"""

    @patch("src.data_loader.HeadHunterAPI")
    @patch("src.data_loader.DBManager")
    def test_load_companies_vacancies(self, mock_db_manager, mock_api):
        """Тест загрузки компаний и вакансий"""
        # Настраиваем моки
        mock_api_instance = Mock()
        mock_api_instance.search_companies.return_value = [{"id": "123", "name": "Yandex"}]
        mock_api_instance.get_company_vacancies.return_value = [
            {"id": "1", "name": "Python Dev", "url": "url1"},
            {"id": "2", "name": "Java Dev", "url": "url2"},
        ]
        mock_api.return_value = mock_api_instance

        mock_db_instance = Mock()
        mock_db_manager.return_value = mock_db_instance

        # Создаем временный файл с компаниями
        with open("test_companies.txt", "w", encoding="utf-8") as f:
            f.write("Yandex\nSber\n")

        # Загружаем данные
        with patch("builtins.open", return_value=open("test_companies.txt", "r", encoding="utf-8")):
            load_companies_vacancies()

        # Проверяем вызовы
        assert mock_api_instance.search_companies.call_count >= 1
        assert mock_api_instance.get_company_vacancies.call_count >= 1
        assert mock_db_instance.insert_employer.call_count >= 1
        assert mock_db_instance.insert_vacancy.call_count >= 2

        # Удаляем временный файл
        import os

        os.remove("test_companies.txt")

    @patch("src.data_loader.HeadHunterAPI")
    @patch("src.data_loader.DBManager")
    def test_load_companies_file_not_found(self, mock_db_manager, mock_api):
        """Тест когда файл companies.txt не найден"""
        mock_api_instance = Mock()
        mock_api_instance.search_companies.return_value = []
        mock_api.return_value = mock_api_instance

        # Должно использовать компании по умолчанию
        load_companies_vacancies()

        assert mock_api_instance.search_companies.call_count >= 1
