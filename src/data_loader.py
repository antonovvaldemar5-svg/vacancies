"""
Модуль для загрузки данных из hh.ru в базу данных.
"""

from src.api import HeadHunterAPI
from src.db_manager import DBManager


def load_companies_vacancies():
    """Загрузка компаний и вакансий в БД"""
    api = HeadHunterAPI()
    db = DBManager()

    # Читаем компании из файла
    try:
        with open("companies.txt", "r", encoding="utf-8") as f:
            companies = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print("Файл companies.txt не найден")
        companies = ["Яндекс", "Сбер", "Тинькофф", "Ozon", "Wildberries", "VK", "Avito", "hh.ru", "2ГИС", "Skyeng"]

    total_vacancies = 0

    for company_name in companies:
        print(f"Обработка: {company_name}")

        # Поиск компании
        companies_data = api.search_companies(company_name)
        if not companies_data:
            print(f"Компания не найдена")
            continue

        company = companies_data[0]
        db.insert_employer(company)

        # Получение вакансий
        vacancies = api.get_company_vacancies(company["id"])

        for vacancy in vacancies:
            vacancy["employer_id"] = company["id"]
            db.insert_vacancy(vacancy)

        print(f"Загружено {len(vacancies)} вакансий")
        total_vacancies += len(vacancies)

    print(f"\nВсего загружено {total_vacancies} вакансий")
    db.close()


if __name__ == "__main__":
    load_companies_vacancies()
