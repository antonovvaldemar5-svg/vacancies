import os
import json
import tempfile
import pytest
from src.file_handlers import JSONSaver, CSVSaver, TXTSaver


class TestJSONSaver:
    """Тесты для класса JSONSaver"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, "test_vacancies.json")
        self.saver = JSONSaver(self.test_file)

    def teardown_method(self):
        """Очистка после каждого теста"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    def test_init_default_filename(self):
        """Тест инициализации с именем файла по умолчанию"""
        saver = JSONSaver()
        assert saver._filename == "vacancies.json"

    def test_init_custom_filename(self):
        """Тест инициализации с кастомным именем файла"""
        assert self.saver._filename == self.test_file

    def test_ensure_file_exists_creates_file(self):
        """Тест создания файла если не существует"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

        saver = JSONSaver(self.test_file)
        assert os.path.exists(self.test_file)

        # Проверяем что файл содержит пустой список
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            assert content == []

    def test_add_vacancy(self):
        """Тест добавления вакансии"""
        vacancy_data = {
            "id": "123",
            "name": "Python Developer",
            "url": "https://hh.ru/vacancy/123",
            "salary_from": 100000,
            "salary_to": 150000
        }

        self.saver.add_vacancy(vacancy_data)

        # Читаем файл и проверяем
        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1
            assert data[0]["id"] == "123"
            assert data[0]["name"] == "Python Developer"

    def test_add_vacancy_no_duplicates(self):
        """Тест что дубликаты не добавляются"""
        vacancy_data = {
            "id": "123",
            "name": "Python Developer"
        }

        # Добавляем два раза
        self.saver.add_vacancy(vacancy_data)
        self.saver.add_vacancy(vacancy_data)

        with open(self.test_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            assert len(data) == 1  # Только одна запись

    def test_get_vacancies_empty(self):
        """Тест получения вакансий из пустого файла"""
        vacancies = self.saver.get_vacancies()
        assert vacancies == []

    def test_get_vacancies_with_data(self):
        """Тест получения вакансий с данными"""
        # Добавляем тестовые данные
        vacancies_data = [
            {"id": "1", "name": "Python", "salary": 100000},
            {"id": "2", "name": "Java", "salary": 120000},
            {"id": "3", "name": "Python Senior", "salary": 200000}
        ]

        for data in vacancies_data:
            self.saver.add_vacancy(data)

        all_vacancies = self.saver.get_vacancies()
        assert len(all_vacancies) == 3

    def test_get_vacancies_with_criteria(self):
        """Тест получения вакансий с критериями"""
        # Добавляем тестовые данные
        vacancies_data = [
            {"id": "1", "name": "Python Developer", "experience": "junior"},
            {"id": "2", "name": "Java Developer", "experience": "senior"},
            {"id": "3", "name": "Python Senior", "experience": "senior"}
        ]

        for data in vacancies_data:
            self.saver.add_vacancy(data)

        # Фильтр по имени
        python_vacancies = self.saver.get_vacancies({"name": "Python"})
        assert len(python_vacancies) == 2

        # Фильтр по опыту
        senior_vacancies = self.saver.get_vacancies({"experience": "senior"})
        assert len(senior_vacancies) == 2

        # Фильтр по нескольким критериям
        python_senior = self.saver.get_vacancies({
            "name": "Python",
            "experience": "senior"
        })
        assert len(python_senior) == 1
        assert python_senior[0]["id"] == "3"

    def test_get_vacancies_case_insensitive(self):
        """Тест регистронезависимого поиска"""
        self.saver.add_vacancy({"id": "1", "name": "Python Developer"})

        # Разные регистры должны находить
        result1 = self.saver.get_vacancies({"name": "python"})
        result2 = self.saver.get_vacancies({"name": "PYTHON"})
        result3 = self.saver.get_vacancies({"name": "Python"})

        assert len(result1) == 1
        assert len(result2) == 1
        assert len(result3) == 1

    def test_delete_vacancy(self):
        """Тест удаления вакансии"""
        # Добавляем несколько вакансий
        vacancies_data = [
            {"id": "1", "name": "Python"},
            {"id": "2", "name": "Java"},
            {"id": "3", "name": "JavaScript"}
        ]

        for data in vacancies_data:
            self.saver.add_vacancy(data)

        # Удаляем одну
        self.saver.delete_vacancy("2")

        # Проверяем
        remaining = self.saver.get_vacancies()
        assert len(remaining) == 2
        ids = [v["id"] for v in remaining]
        assert "1" in ids
        assert "3" in ids
        assert "2" not in ids

    def test_delete_nonexistent_vacancy(self):
        """Тест удаления несуществующей вакансии"""
        self.saver.add_vacancy({"id": "1", "name": "Python"})

        # Удаляем несуществующую - не должно быть ошибки
        self.saver.delete_vacancy("999")

        remaining = self.saver.get_vacancies()
        assert len(remaining) == 1

    def test_read_file_corrupted_json(self):
        """Тест чтения поврежденного JSON файла"""
        # Записываем некорректный JSON
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("{invalid json")

        # Должен вернуть пустой список
        vacancies = self.saver.get_vacancies()
        assert vacancies == []


class TestOtherSavers:
    """Тесты для других саверов (заглушки)"""

    def test_csv_saver_stubs(self):
        """Тест что CSV савер имеет заглушки"""
        saver = CSVSaver()

        with pytest.raises(NotImplementedError):
            saver.add_vacancy({})

        with pytest.raises(NotImplementedError):
            saver.get_vacancies()

        with pytest.raises(NotImplementedError):
            saver.delete_vacancy("1")

    def test_txt_saver_stubs(self):
        """Тест что TXT савер имеет заглушки"""
        saver = TXTSaver()

        with pytest.raises(NotImplementedError):
            saver.add_vacancy({})

        with pytest.raises(NotImplementedError):
            saver.get_vacancies()

        with pytest.raises(NotImplementedError):
            saver.delete_vacancy("1")
