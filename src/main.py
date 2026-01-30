import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api import HeadHunterAPI
from src.vacancy import Vacancy
from src.file_handlers import JSONSaver
from src.utils import (
    filter_vacancies,
    get_vacancies_by_salary,
    sort_vacancies,
    get_top_vacancies,
    print_vacancies
)


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль
    """
    print("=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU")
    print("=" * 60)

    # Инициализация API и хранилища
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    while True:
        print("\nМЕНЮ:")
        print("1. Поиск и сохранение вакансий")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Поиск вакансий по ключевому слову")
        print("4. Поиск по диапазону зарплат")
        print("5. Показать все сохраненные вакансии")
        print("6. Удалить вакансию")
        print("7. Очистить все сохраненные вакансии")
        print("8. Выход")

        choice = input("\nВыберите действие (1-8): ").strip()

        if choice == "1":
            # Поиск и сохранение вакансий
            search_query = input("Введите поисковый запрос (например: Python разработчик): ").strip()
            if not search_query:
                print("Поисковый запрос не может быть пустым")
                continue

            per_page = input("Введите количество вакансий для загрузки (по умолчанию 100): ").strip()
            per_page = int(per_page) if per_page.isdigit() else 100

            print("\nЗагружаем вакансии...")
            vacancies_data = hh_api.get_vacancies(search_query, per_page=per_page)

            if not vacancies_data:
                print("Вакансии не найдены")
                continue

            # Преобразование в объекты
            vacancies_list = Vacancy.cast_to_object_list(vacancies_data)

            # Сохранение в файл
            for vacancy in vacancies_list:
                json_saver.add_vacancy(vacancy.to_dict())

            print(f"\nЗагружено и сохранено {len(vacancies_list)} вакансий")

            # Показать первые 5
            show = input("Показать первые 5 вакансий? (y/n): ").lower()
            if show == 'y':
                print_vacancies(vacancies_list[:5])

        elif choice == "2":
            # Топ N вакансий по зарплате
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N: ").strip())

                # Получение из файла
                saved_data = json_saver.get_vacancies()
                if not saved_data:
                    print("Нет сохраненных вакансий")
                    continue

                vacancies_list = Vacancy.cast_to_object_list(saved_data)
                sorted_vacancies = sort_vacancies(vacancies_list)
                top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

                print(f"\nТоп {top_n} вакансий по зарплате:")
                print_vacancies(top_vacancies)

            except ValueError:
                print("Некорректное число")

        elif choice == "3":
            # Поиск по ключевому слову
            keyword = input("Введите ключевое слово для поиска в описании: ").strip()

            if not keyword:
                print("Ключевое слово не может быть пустым")
                continue

            # Получение из файла и фильтрация
            saved_data = json_saver.get_vacancies()
            if not saved_data:
                print("Нет сохраненных вакансий")
                continue

            vacancies_list = Vacancy.cast_to_object_list(saved_data)
            filtered = filter_vacancies(vacancies_list, [keyword])

            if not filtered:
                print(f"Вакансии с ключевым словом '{keyword}' не найдены")
            else:
                print(f"\nНайдено {len(filtered)} вакансий с ключевым словом '{keyword}':")
                print_vacancies(filtered)

        elif choice == "4":
            # Поиск по диапазону зарплат
            salary_range = input("Введите диапазон зарплат (например: 100000-200000): ").strip()

            if not salary_range:
                print("Диапазон зарплат не может быть пустым")
                continue

            # Получение из файла и фильтрация
            saved_data = json_saver.get_vacancies()
            if not saved_data:
                print("Нет сохраненных вакансий")
                continue

            vacancies_list = Vacancy.cast_to_object_list(saved_data)
            filtered = get_vacancies_by_salary(vacancies_list, salary_range)

            if not filtered:
                print(f"Вакансии с зарплатой в диапазоне {salary_range} не найдены")
            else:
                print(f"\nНайдено {len(filtered)} вакансий с зарплатой в диапазоне {salary_range}:")
                print_vacancies(filtered)

        elif choice == "5":
            # Показать все сохраненные вакансии
            saved_data = json_saver.get_vacancies()

            if not saved_data:
                print("Нет сохраненных вакансий")
                continue

            vacancies_list = Vacancy.cast_to_object_list(saved_data)
            print(f"\nВсе сохраненные вакансии ({len(vacancies_list)} шт.):")

            show_all = input("Показать все сразу? (y/n): ").lower()
            if show_all == 'y':
                print_vacancies(vacancies_list)
            else:
                # Показать с пагинацией
                page_size = 5
                for i in range(0, len(vacancies_list), page_size):
                    page = vacancies_list[i:i + page_size]
                    print_vacancies(page)

                    if i + page_size < len(vacancies_list):
                        input("Нажмите Enter для продолжения...")

        elif choice == "6":
            # Удаление вакансии
            vacancy_id = input("Введите ID вакансии для удаления: ").strip()

            if vacancy_id:
                json_saver.delete_vacancy(vacancy_id)
                print(f"Вакансия с ID {vacancy_id} удалена")
            else:
                print("ID вакансии не может быть пустым")

        elif choice == "7":
            # Очистка всех вакансий
            confirm = input("Вы уверены, что хотите удалить все вакансии? (y/n): ").lower()
            if confirm == 'y':
                json_saver.clear_file()
                print("Все вакансии удалены")

        elif choice == "8":
            print("Выход из программы...")
            break

        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
