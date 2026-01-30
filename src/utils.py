from typing import List, Optional
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
        vacancy_text = " ".join([
            vacancy._name or "",
            vacancy._description or "",
            vacancy._experience or "",
            vacancy._employer or ""
        ]).lower()

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
    if not salary_range:
        return vacancies

    try:
        # Поддержка разных форматов
        if "-" in salary_range:
            parts = salary_range.replace(" ", "").split("-")
            min_salary = int(parts[0])
            max_salary = int(parts[1]) if len(parts) > 1 else float('inf')
        elif " " in salary_range:
            parts = salary_range.split()
            min_salary = int(parts[0])
            max_salary = int(parts[2]) if len(parts) > 2 else float('inf')
        else:
            min_salary = int(salary_range)
            max_salary = float('inf')

        return [
            vacancy for vacancy in vacancies
            if vacancy.salary_to >= min_salary and vacancy.salary_from <= max_salary
        ]
    except ValueError:
        print("Некорректный формат диапазона зарплат")
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
    return vacancies[:top_n]


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
