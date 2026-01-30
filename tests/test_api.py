import pytest
from unittest.mock import Mock, patch
from src.api import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.api = HeadHunterAPI()
        self.search_query = "Python разработчик"

    def test_init(self):
        """Тест инициализации"""
        assert self.api._base_url == "https://api.hh.ru/vacancies"
        assert "User-Agent" in self.api._headers

    @patch('requests.get')
    def test_get_vacancies_success(self, mock_get):
        """Тест успешного получения вакансий"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "123",
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/123",
                    "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
                    "snippet": {"requirement": "Опыт работы от 3 лет"},
                    "experience": {"name": "От 1 года до 3 лет"},
                    "employer": {"name": "Test Company"},
                    "published_at": "2024-01-01T10:00:00+0300"
                }
            ]
        }
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies(self.search_query, per_page=1)

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        assert vacancies[0]["salary_from"] == 100000  # Изменили с "salary" на "salary_from"
        assert vacancies[0]["salary_to"] == 150000
        assert vacancies[0]["salary_currency"] == "RUR"

    @patch('requests.get')
    def test_get_vacancies_without_salary(self, mock_get):
        """Тест получения вакансий без зарплаты"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [
                {
                    "id": "124",
                    "name": "Python Developer",
                    "alternate_url": "https://hh.ru/vacancy/124",
                    "salary": None,
                    "snippet": {"requirement": "Опыт работы"},
                    "experience": {"name": "Нет опыта"},
                    "employer": {"name": "Test Company"},
                    "published_at": "2024-01-01T10:00:00+0300"
                }
            ]
        }
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies(self.search_query)

        assert len(vacancies) == 1
        assert vacancies[0]["salary_from"] is None  # Изменили с "salary" на "salary_from"
        assert vacancies[0]["salary_to"] is None
        assert vacancies[0]["salary_currency"] is None

    @patch('requests.get')
    def test_get_vacancies_empty_response(self, mock_get):
        """Тест пустого ответа"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies(self.search_query)

        assert len(vacancies) == 0

    def test_clean_description(self):
        """Тест очистки описания от HTML"""
        dirty_html = "Требуется <strong>Python</strong> разработчик <br/> с опытом"
        clean_text = self.api._clean_description(dirty_html)

        assert "<strong>" not in clean_text
        assert "<br/>" not in clean_text
        assert "Python" in clean_text

    def test_clean_description_empty(self):
        """Тест очистки пустого описания"""
        assert self.api._clean_description("") == ""
        assert self.api._clean_description(None) == ""

    @patch('requests.get')
    def test_get_vacancies_with_params(self, mock_get):
        """Тест получения вакансий с параметрами"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"items": []}
        mock_get.return_value = mock_response

        self.api.get_vacancies(
            self.search_query,
            per_page=50,
            page=2,
            only_with_salary=True
        )

        # Проверяем переданные параметры
        call_args = mock_get.call_args
        params = call_args[1]['params']

        assert params["text"] == self.search_query
        assert params["per_page"] == 50
        assert params["page"] == 2
        assert params["area"] == 113  # Россия

    @patch('requests.get')
    def test_get_vacancies_request_exception(self, mock_get):
        """Тест исключения при запросе"""
        mock_get.side_effect = Exception("Connection error")

        vacancies = self.api.get_vacancies(self.search_query)
        assert vacancies == []

    @patch('requests.get')
    def test_get_vacancies_json_exception(self, mock_get):
        """Тест исключения при парсинге JSON"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = Exception("JSON error")
        mock_get.return_value = mock_response

        vacancies = self.api.get_vacancies(self.search_query)
        assert vacancies == []
