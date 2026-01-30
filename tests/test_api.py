import pytest
from unittest.mock import Mock, patch
from src.api import HeadHunterAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_api_initialization(self):
        """Тест инициализации API"""
        api = HeadHunterAPI()
        assert api._base_url == "https://api.hh.ru/vacancies"
        assert "User-Agent" in api._headers

    @patch('requests.get')
    def test_connect_success(self, mock_get):
        """Тест успешного подключения"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        api.connect()  # Не должно вызывать исключение

        mock_get.assert_called_once()

    @patch('requests.get')
    def test_connect_failure(self, mock_get):
        """Тест неудачного подключения"""
        mock_get.side_effect = Exception("Connection error")

        api = HeadHunterAPI()
        with pytest.raises(ConnectionError):
            api.connect()

    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        """Тест получения вакансий"""
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
                    "published_at": "2024-01-01T00:00:00"
                }
            ]
        }
        mock_get.return_value = mock_response

        api = HeadHunterAPI()
        vacancies = api.get_vacancies("Python")

        assert len(vacancies) == 1
        assert vacancies[0]["name"] == "Python Developer"
        assert vacancies[0]["salary"]["from"] == 100000

    def test_clean_description(self):
        """Тест очистки описания от HTML тегов"""
        api = HeadHunterAPI()

        dirty_text = "Требуется <strong>Python</strong> разработчик"
        clean_text = api._clean_description(dirty_text)

        assert clean_text == "Требуется Python разработчик"
        assert "<" not in clean_text
        assert ">" not in clean_text
