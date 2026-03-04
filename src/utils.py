"""
Модуль с утилитными функциями для работы с вакансиями.
"""

from typing import List

from .vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрация вакансий по ключевым словам

    Args:
        vacancies: Список вакансий
        filter_words: Список ключевых слов

    Returns:
        Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        vacancy_text = " ".join(
            [
                vacancy._name or "",
                vacancy._description or "",
                vacancy._experience or "",
                vacancy._employer or "",
            ]
        ).lower()

        if any(word.lower() in vacancy_text for word in filter_words):
            filtered.append(vacancy)

    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтрация вакансий по диапазону зарплат

    Args:
        vacancies: Список вакансий
        salary_range: Диапазон зарплат в формате "100000-150000"

    Returns:
        Отфильтрованный список вакансий
    """
    if not salary_range or salary_range.strip() == "":
        return vacancies

    try:
        # Поддержка разных форматов
        salary_range = salary_range.strip()

        # Удаляем возможные пробелы вокруг дефиса
        if "-" in salary_range:
            parts = salary_range.replace(" ", "").split("-")
            min_salary = int(parts[0])
            max_salary = int(parts[1]) if len(parts) > 1 else float("inf")
        else:
            # Если только одно число, ищем зарплату ОТ этого числа
            min_salary = int(salary_range)
            max_salary = float("inf")

        filtered = []
        for vacancy in vacancies:
            # Вакансия без зарплаты не подходит для фильтра по зарплате
            if vacancy.salary_from == 0 and vacancy.salary_to == 0:
                continue

            # Получаем минимальную и максимальную зарплату вакансии
            vacancy_min = vacancy.salary_from
            vacancy_max = vacancy.salary_to if vacancy.salary_to > 0 else vacancy.salary_from

            # Вакансия подходит если ее диапазон пересекается с запрошенным
            # vacancy_min <= max_salary AND vacancy_max >= min_salary
            if vacancy_min <= max_salary and vacancy_max >= min_salary:
                filtered.append(vacancy)

        return filtered

    except ValueError:
        # При ошибке парсинга числа возвращаем все вакансии
        return vacancies


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортировка вакансий по убыванию зарплаты

    Args:
        vacancies: Список вакансий

    Returns:
        Отсортированный список вакансий
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Получение топ N вакансий

    Args:
        vacancies: Список вакансий
        top_n: Количество вакансий для вывода

    Returns:
        Список топ N вакансий
    """
    return vacancies[:top_n] if top_n > 0 else []


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Вывод вакансий в читаемом формате

    Args:
        vacancies: Список вакансий
    """
    if not vacancies:
        print("Вакансии не найдены")
        return

    for i, vacancy in enumerate(vacancies, 1):
        print(f"\n{'=' * 50}")
        print(f"Вакансия #{i}")
        print(str(vacancy))
    print(f"\n{'=' * 50}")
    print(f"Найдено вакансий: {len(vacancies)}")
