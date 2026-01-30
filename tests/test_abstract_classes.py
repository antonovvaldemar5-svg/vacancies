import pytest
from src.abstract_classes import APIHandler, FileHandler


class TestAbstractClasses:
    """Тесты абстрактных классов"""

    def test_api_handler_is_abstract(self):
        """Тест что APIHandler абстрактный"""
        # Нельзя создать экземпляр абстрактного класса
        with pytest.raises(TypeError):
            APIHandler()

    def test_api_handler_methods_are_abstract(self):
        """Тест что методы APIHandler абстрактные"""
        # Проверяем декораторы методов
        assert hasattr(APIHandler.get_vacancies, '__isabstractmethod__')
        assert APIHandler.get_vacancies.__isabstractmethod__ is True

    def test_file_handler_is_abstract(self):
        """Тест что FileHandler абстрактный"""
        with pytest.raises(TypeError):
            FileHandler()

    def test_file_handler_methods_are_abstract(self):
        """Тест что методы FileHandler абстрактные"""
        assert hasattr(FileHandler.add_vacancy, '__isabstractmethod__')
        assert FileHandler.add_vacancy.__isabstractmethod__ is True

        assert hasattr(FileHandler.get_vacancies, '__isabstractmethod__')
        assert FileHandler.get_vacancies.__isabstractmethod__ is True

        assert hasattr(FileHandler.delete_vacancy, '__isabstractmethod__')
        assert FileHandler.delete_vacancy.__isabstractmethod__ is True

        assert hasattr(FileHandler.clear_file, '__isabstractmethod__')
        assert FileHandler.clear_file.__isabstractmethod__ is True
