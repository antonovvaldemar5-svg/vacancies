import pytest
import json
import os
from unittest.mock import mock_open, patch
from src.file_handlers import JSONSaver


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    def test_initialization(self):
        """Тест инициализации JSONSaver"""
        saver = JSONSaver("test_vacancies.json")
        assert saver._filename == "test_vacancies.json"

        # С файлом по умолчанию
        saver_default = JSONSaver()
        assert saver_default._filename == "vacancies.json"

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open)
    def test_ensure_file_exists_creates_file(self, mock_file, mock_exists):
        """Тест создания файла если его нет"""
        mock_exists.return_value = False

        saver = JSONSaver("test.json")
        saver._ensure_file_exists()

        mock_file.assert_called_once_with("test.json", 'w', encoding='utf-8')
        mock_file().write.assert_called_once()

    @patch('os.path.exists')
    def test_ensure_file_exists_does_nothing(self, mock_exists):
        """Тест когда файл уже существует"""
        mock_exists.return_value = True

        saver = JSONSaver("test.json")
        saver._ensure_file_exists()  # Не должно создавать файл

    @patch('builtins.open', new_callable=mock_open, read_data='[{"id": "1", "name": "Test"}]')
    def test_read_file(self, mock_file):
        """Тест чтения файла"""
        saver = JSONSaver("test.json")
        data = saver._read_file()

        assert data == [{"id": "1", "name": "Test"}]
        mock_file.assert_called_once_with("test.json", 'r', encoding='utf-8')

    @patch('builtins.open', new_callable=mock_open)
    def test_write_file(self, mock_file):
        """Тест записи в файл"""
        saver = JSONSaver("test.json")
        test_data = [{"id": "1", "name": "Test"}]

        saver._write_file(test_data)

        mock_file.assert_called_once_with("test.json", 'w', encoding='utf-8')
        # Проверяем что json.dump был вызван с правильными аргументами
        mock_file().write.assert_called_once()

    def test_add_vacancy_no_duplicate(self):
        """Тест добавления вакансии без дубликата"""
        saver = JSONSaver("test.json")

        # Мокаем чтение и запись
        with patch.object(saver, '_read_file', return_value=[]):
            with patch.object(saver, '_write_file') as mock_write:
                vacancy_data = {"id": "123", "name": "Python Developer"}
                saver.add_vacancy(vacancy_data)

                mock_write.assert_called_once_with([vacancy_data])

    def test_add_vacancy_with_duplicate(self):
        """Тест добавления вакансии с дубликатом"""
        saver = JSONSaver("test.json")

        existing_vacancies = [{"id": "123", "name": "Existing"}]

        with patch.object(saver, '_read_file', return_value=existing_vacancies):
            with patch.object(saver, '_write_file') as mock_write:
                vacancy_data = {"id": "123", "name": "Duplicate"}  # Тот же ID
                saver.add_vacancy(vacancy_data)

                # Не должно вызывать запись так как дубликат
                mock_write.assert_not_called()

    def test_get_vacancies_no_criteria(self):
        """Тест получения всех вакансий"""
        saver = JSONSaver("test.json")
        test_data = [
            {"id": "1", "name": "Python"},
            {"id": "2", "name": "Java"}
        ]

        with patch.object(saver, '_read_file', return_value=test_data):
            result = saver.get_vacancies()

            assert result == test_data
            assert len(result) == 2

    def test_get_vacancies_with_criteria(self):
        """Тест получения вакансий по критериям"""
        saver = JSONSaver("test.json")
        test_data = [
            {"id": "1", "name": "Python Developer", "experience": "Junior"},
            {"id": "2", "name": "Java Developer", "experience": "Senior"},
            {"id": "3", "name": "Python Senior", "experience": "Senior"}
        ]

        with patch.object(saver, '_read_file', return_value=test_data):
            # Поиск по имени
            result = saver.get_vacancies({"name": "Python"})
            assert len(result) == 2

            # Поиск по опыту
            result = saver.get_vacancies({"experience": "Senior"})
            assert len(result) == 2
            assert result[0]["name"] == "Java Developer"

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        saver = JSONSaver("test.json")
        test_data = [
            {"id": "1", "name": "Python"},
            {"id": "2", "name": "Java"},
            {"id": "3", "name": "C++"}
        ]

        with patch.object(saver, '_read_file', return_value=test_data):
            with patch.object(saver, '_write_file') as mock_write:
                saver.delete_vacancy("2")

                # Должны остаться вакансии с id 1 и 3
                expected_data = [
                    {"id": "1", "name": "Python"},
                    {"id": "3", "name": "C++"}
                ]
                mock_write.assert_called_once_with(expected_data)
