from src.db_creator import DBCreator
from src.db_manager import DBManager
from src.data_loader import load_companies_vacancies


def print_vacancies(vacancies):
    """Вывод вакансий в читаемом виде"""
    if not vacancies:
        print("Вакансии не найдены")
        return

    for i, v in enumerate(vacancies, 1):
        print(f"\n--- Вакансия {i} ---")
        print(f"Компания: {v['company_name']}")
        print(f"Вакансия: {v['vacancy_name']}")

        salary_from = v.get("salary_from")
        salary_to = v.get("salary_to")
        currency = v.get("salary_currency", "руб")

        if salary_from and salary_to:
            print(f"Зарплата: {
                  salary_from:,} - {salary_to:,} {currency}".replace(",", " "))
        elif salary_from:
            print(f"Зарплата: от {salary_from:,} {currency}".replace(",", " "))
        elif salary_to:
            print(f"Зарплата: до {salary_to:,} {currency}".replace(",", " "))
        else:
            print("Зарплата: не указана")

        print(f"Ссылка: {v['url']}")

    print(f"\nВсего: {len(vacancies)} вакансий")


def print_companies_stats(stats):
    """Вывод статистики по компаниям"""
    print("\n" + "=" * 60)
    print("КОМПАНИИ И КОЛИЧЕСТВО ВАКАНСИЙ")
    print("=" * 60)

    for s in stats:
        print(f"{s['company_name']}: {s['vacancies_count']} вакансий")

    total = sum(s["vacancies_count"] for s in stats)
    print(f"\nВсего компаний: {len(stats)}, всего вакансий: {total}")


def user_interaction():
    """Интерфейс пользователя"""
    print("=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU (БД версия)")
    print("=" * 60)

    db = None

    while True:
        print("\nМЕНЮ:")
        print("1. Создать таблицы в БД")
        print("2. Загрузить данные из hh.ru")
        print("3. Список компаний и количество вакансий")
        print("4. Все вакансии")
        print("5. Средняя зарплата")
        print("6. Вакансии с зарплатой выше средней")
        print("7. Поиск вакансий по ключевому слову")
        print("8. Выход")

        choice = input("\nВыберите действие (1-8): ").strip()

        if choice == "1":
            DBCreator.create_tables()
            db = DBManager()

        elif choice == "2":
            load_companies_vacancies()
            if not db:
                db = DBManager()

        elif choice == "3":
            if not db:
                print("Сначала загрузите данные (пункт 2)")
                continue
            stats = db.get_companies_and_vacancies_count()
            print_companies_stats(stats)

        elif choice == "4":
            if not db:
                print("Сначала загрузите данные (пункт 2)")
                continue
            vacancies = db.get_all_vacancies()
            print_vacancies(vacancies)

        elif choice == "5":
            if not db:
                print("Сначала загрузите данные (пункт 2)")
                continue
            avg = db.get_avg_salary()
            print(f"\nСредняя зарплата: {avg:,.0f} руб.".replace(",", " "))

        elif choice == "6":
            if not db:
                print("Сначала загрузите данные (пункт 2)")
                continue
            vacancies = db.get_vacancies_with_higher_salary()
            print(f"\nНайдено {
                len(vacancies)} вакансий с зарплатой выше средней")
            print_vacancies(vacancies)

        elif choice == "7":
            if not db:
                print("Сначала загрузите данные (пункт 2)")
                continue
            keyword = input("🔍 Введите ключевое слово: ").strip()
            vacancies = db.get_vacancies_with_keyword(keyword)
            print(f"\nНайдено {len(vacancies)} вакансий со словом '{keyword}'")
            print_vacancies(vacancies)

        elif choice == "8":
            if db:
                db.close()
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
