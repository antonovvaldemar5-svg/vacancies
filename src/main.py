"""
Основной модуль для взаимодействия с пользователем.
"""
from src.db_creator import DBCreator
from src.db_manager import DBManager
from src.data_loader import load_companies_vacancies


def print_menu() -> None:
    """Вывод главного меню программы."""
    print("\n" + "=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU (PostgreSQL версия)")
    print("=" * 60)
    print("\nМЕНЮ:")
    print("1. Создать базу данных и таблицы")
    print("2. Загрузить данные из hh.ru")
    print("3. Показать компании и количество вакансий")
    print("4. Показать все вакансии")
    print("5. Показать среднюю зарплату")
    print("6. Показать вакансии с зарплатой выше средней")
    print("7. Поиск вакансий по ключевому слову")
    print("8. Выход")


def handle_database_creation() -> DBManager:
    """
    Обработка создания базы данных и таблиц.

    Returns:
        DBManager: Экземпляр класса для работы с БД
    """
    print("\n" + "=" * 60)
    print("СОЗДАНИЕ БАЗЫ ДАННЫХ И ТАБЛИЦ")
    print("=" * 60)

    if DBCreator.create_database():
        DBCreator.create_tables()
        return DBManager()
    return None


def handle_data_loading(db: DBManager) -> DBManager:
    """
    Обработка загрузки данных из hh.ru.

    Args:
        db: Экземпляр DBManager или None

    Returns:
        DBManager: Экземпляр класса для работы с БД
    """
    print("\n" + "=" * 60)
    print("ЗАГРУЗКА ДАННЫХ ИЗ HH.RU")
    print("=" * 60)

    load_companies_vacancies()
    if not db:
        db = DBManager()
    return db


def show_companies_stats(db: DBManager) -> None:
    """
    Вывод статистики по компаниям.

    Args:
        db: Экземпляр DBManager для работы с БД
    """
    if not db:
        print("Сначала загрузите данные (пункт 2)")
        return

    stats = db.get_companies_and_vacancies_count()
    if not stats:
        print("Нет данных о компаниях")
        return

    print("\n" + "=" * 60)
    print("КОМПАНИИ И КОЛИЧЕСТВО ВАКАНСИЙ")
    print("=" * 60)

    for s in stats:
        print(f"{s['company_name']}: {s['vacancies_count']} вакансий")

    total = sum(s['vacancies_count'] for s in stats)
    print(f"\nВсего компаний: {len(stats)}, всего вакансий: {total}")


def show_all_vacancies(db: DBManager) -> None:
    """
    Вывод всех вакансий.

    Args:
        db: Экземпляр DBManager для работы с БД
    """
    if not db:
        print("Сначала загрузите данные (пункт 2)")
        return

    vacancies = db.get_all_vacancies()
    if not vacancies:
        print("Вакансии не найдены")
        return

    print("\n" + "=" * 60)
    print("ВСЕ ВАКАНСИИ")
    print("=" * 60)

    for i, v in enumerate(vacancies, 1):
        print(f"\n--- Вакансия {i} ---")
        print(f"Компания: {v['company_name']}")
        print(f"Вакансия: {v['vacancy_name']}")

        salary_from = v.get('salary_from')
        salary_to = v.get('salary_to')
        currency = v.get('salary_currency', 'руб')

        if salary_from and salary_to:
            salary_str = f"{salary_from:,} - {salary_to:,} {currency}"
            print(f"Зарплата: {salary_str.replace(',', ' ')}")
        elif salary_from:
            salary_str = f"от {salary_from:,} {currency}"
            print(f"Зарплата: {salary_str.replace(',', ' ')}")
        elif salary_to:
            salary_str = f"до {salary_to:,} {currency}"
            print(f"Зарплата: {salary_str.replace(',', ' ')}")
        else:
            print("Зарплата: не указана")

        print(f"Ссылка: {v['url']}")

    print(f"\nВсего: {len(vacancies)} вакансий")


def show_average_salary(db: DBManager) -> None:
    """
    Вывод средней зарплаты.

    Args:
        db: Экземпляр DBManager для работы с БД
    """
    if not db:
        print("Сначала загрузите данные (пункт 2)")
        return

    avg = db.get_avg_salary()
    if avg:
        salary_str = f"{avg:,.0f} руб."
        print(f"\nСредняя зарплата: {salary_str.replace(',', ' ')}")
    else:
        print("\nНет данных о зарплатах")


def show_higher_salary_vacancies(db: DBManager) -> None:
    """
    Вывод вакансий с зарплатой выше средней.

    Args:
        db: Экземпляр DBManager для работы с БД
    """
    if not db:
        print("Сначала загрузите данные (пункт 2)")
        return

    vacancies = db.get_vacancies_with_higher_salary()
    if not vacancies:
        print("\nВакансии с зарплатой выше средней не найдены")
        return

    print(f"\nНайдено {len(vacancies)} вакансий с зарплатой выше средней")
    show_all_vacancies(db)  # Переиспользуем существующую функцию


def search_vacancies_by_keyword(db: DBManager) -> None:
    """
    Поиск вакансий по ключевому слову.

    Args:
        db: Экземпляр DBManager для работы с БД
    """
    if not db:
        print("Сначала загрузите данные (пункт 2)")
        return

    keyword = input("Введите ключевое слово для поиска: ").strip()
    if not keyword:
        print("Ключевое слово не может быть пустым")
        return

    vacancies = db.get_vacancies_with_keyword(keyword)
    if not vacancies:
        print(f"Вакансии с ключевым словом '{keyword}' не найдены")
        return

    print(f"\nНайдено {len(vacancies)} вакансий со словом '{keyword}'")
    show_all_vacancies(db)  # Переиспользуем существующую функцию


def user_interaction() -> None:
    """
    Основная функция взаимодействия с пользователем.

    Запускает цикл меню и обрабатывает выбор пользователя.
    """
    db = None

    while True:
        print_menu()
        choice = input("\nВыберите действие (1-8): ").strip()

        if choice == "1":
            db = handle_database_creation()

        elif choice == "2":
            db = handle_data_loading(db)

        elif choice == "3":
            show_companies_stats(db)

        elif choice == "4":
            show_all_vacancies(db)

        elif choice == "5":
            show_average_salary(db)

        elif choice == "6":
            show_higher_salary_vacancies(db)

        elif choice == "7":
            search_vacancies_by_keyword(db)

        elif choice == "8":
            if db:
                db.close()
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
