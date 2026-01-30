import pytest
from abc import ABC
from src.abstract_classes import APIHandler, FileHandler


class TestAbstractClasses:
    """Тесты для абстрактных классов"""

    def test_api_handler_is_abstract(self):
        """Проверка, что APIHandler - абстрактный класс"""
        assert issubclass(APIHandler, ABC)

        # Нельзя создать экземпляр
        with pytest.raises(TypeError):
            APIHandler()

    def test_file_handler_is_abstract(self):
        """Проверка, что FileHandler - абстрактный класс"""
        assert issubclass(FileHandler, ABC)

        with pytest.raises(TypeError):
            FileHandler()

    def test_api_handler_methods(self):
        """Проверка наличия абстрактных методов в APIHandler"""
        assert hasattr(APIHandler, 'connect')
        assert hasattr(APIHandler, 'get_vacancies')
        assert APIHandler.connect.__isabstractmethod__
        assert APIHandler.get_vacancies.__isabstractmethod__

    def test_file_handler_methods(self):
        """Проверка наличия абстрактных методов в FileHandler"""
        assert hasattr(FileHandler, 'add_vacancy')
        assert hasattr(FileHandler, 'get_vacancies')
        assert hasattr(FileHandler, 'delete_vacancy')
        assert FileHandler.add_vacancy.__isabstractmethod__
        assert FileHandler.get_vacancies.__isabstractmethod__
        assert FileHandler.delete_vacancy.__isabstractmethod__
