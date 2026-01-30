"""
Модуль для взаимодействия с пользователем через консоль.
Основной интерфейс программы.
"""
import os
import sys

# Добавляем родительскую директорию в путь для корректных импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.api import HeadHunterAPI
    from src.file_handlers import JSONSaver
    from src.utils import (
        filter_vacancies,
        get_top_vacancies,
        get_vacancies_by_salary,
        print_vacancies,
        sort_vacancies,
    )
    from src.vacancy import Vacancy
except ImportError as e:
    print(f"Ошибка импорта модулей: {e}")
    print("Проверьте структуру проекта и наличие всех файлов.")
    sys.exit(1)


def user_interaction() -> None:
    """
    Функция для взаимодействия с пользователем через консоль.
    Предоставляет меню с различными опциями работы с вакансиями.
    """
    print("=" * 60)
    print("ПОИСК ВАКАНСИЙ НА HH.RU")
    print("=" * 60)

    # Инициализация API и хранилища
    hh_api = HeadHunterAPI()
    json_saver = JSONSaver()

    while True:
        try:
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
                _handle_search_vacancies(hh_api, json_saver)
            elif choice == "2":
                _handle_top_vacancies(json_saver)
            elif choice == "3":
                _handle_keyword_search(json_saver)
            elif choice == "4":
                _handle_salary_search(json_saver)
            elif choice == "5":
                _handle_show_all(json_saver)
            elif choice == "6":
                _handle_delete_vacancy(json_saver)
            elif choice == "7":
                _handle_clear_all(json_saver)
            elif choice == "8":
                print("Выход из программы...")
                break
            else:
                print("Некорректный выбор. Попробуйте снова.")

        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            print("Попробуйте еще раз.")


def _handle_search_vacancies(api: HeadHunterAPI, saver: JSONSaver) -> None:
    """Обработка поиска и сохранения вакансий"""
    search_query = input(
        "Введите поисковый запрос (например: Python разработчик): "
    ).strip()

    if not search_query:
        print("Поисковый запрос не может быть пустым")
        return

    try:
        per_page_input = input(
            "Введите количество вакансий для загрузки (по умолчанию 100): "
        ).strip()
        per_page = int(per_page_input) if per_page_input.isdigit() else 100
    except ValueError:
        print("Некорректное число, используется значение по умолчанию (100)")
        per_page = 100

    print("\nЗагружаем вакансии...")
    try:
        vacancies_data = api.get_vacancies(search_query, per_page=per_page)
    except Exception as e:
        print(f"Ошибка при загрузке вакансий: {e}")
        return

    if not vacancies_data:
        print("Вакансии не найдены")
        return

    # Преобразование в объекты
    try:
        vacancies_list = Vacancy.cast_to_object_list(vacancies_data)
    except Exception as e:
        print(f"Ошибка при обработке данных вакансий: {e}")
        return

    # Сохранение в файл
    saved_count = 0
    for vacancy in vacancies_list:
        try:
            saver.add_vacancy(vacancy.to_dict())
            saved_count += 1
        except Exception as e:
            print(f"Ошибка при сохранении вакансии {vacancy._name}: {e}")

    print(f"\nЗагружено {len(vacancies_list)} вакансий, сохранено {saved_count}")

    # Показать первые 5
    if vacancies_list:
        show = input("Показать первые 5 вакансий? (y/n): ").lower()
        if show == 'y':
            print_vacancies(vacancies_list[:5])


def _handle_top_vacancies(saver: JSONSaver) -> None:
    """Обработка получения топ N вакансий"""
    try:
        top_n_input = input("Введите количество вакансий для вывода в топ N: ").strip()
        if not top_n_input:
            print("Значение не может быть пустым")
            return

        top_n = int(top_n_input)
        if top_n <= 0:
            print("Число должно быть положительным")
            return
    except ValueError:
        print("Некорректное число")
        return

    # Получение из файла
    try:
        saved_data = saver.get_vacancies()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    if not saved_data:
        print("Нет сохраненных вакансий")
        return

    try:
        vacancies_list = Vacancy.cast_to_object_list(saved_data)
        sorted_vacancies = sort_vacancies(vacancies_list)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        print(f"\nТоп {top_n} вакансий по зарплате:")
        print_vacancies(top_vacancies)
    except Exception as e:
        print(f"Ошибка при обработке вакансий: {e}")


def _handle_keyword_search(saver: JSONSaver) -> None:
    """Обработка поиска по ключевому слову"""
    keyword = input("Введите ключевое слово для поиска в описании: ").strip()

    if not keyword:
        print("Ключевое слово не может быть пустым")
        return

    # Получение из файла
    try:
        saved_data = saver.get_vacancies()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    if not saved_data:
        print("Нет сохраненных вакансий")
        return

    try:
        vacancies_list = Vacancy.cast_to_object_list(saved_data)
        filtered = filter_vacancies(vacancies_list, [keyword])

        if not filtered:
            print(f"Вакансии с ключевым словом '{keyword}' не найдены")
        else:
            print(f"\nНайдено {len(filtered)} вакансий с ключевым словом '{keyword}':")
            print_vacancies(filtered)
    except Exception as e:
        print(f"Ошибка при фильтрации вакансий: {e}")


def _handle_salary_search(saver: JSONSaver) -> None:
    """Обработка поиска по диапазону зарплат"""
    salary_range = input(
        "Введите диапазон зарплат (например: 100000-200000): "
    ).strip()

    if not salary_range:
        print("Диапазон зарплат не может быть пустым")
        return

    # Получение из файла
    try:
        saved_data = saver.get_vacancies()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    if not saved_data:
        print("Нет сохраненных вакансий")
        return

    try:
        vacancies_list = Vacancy.cast_to_object_list(saved_data)
        filtered = get_vacancies_by_salary(vacancies_list, salary_range)

        if not filtered:
            print(f"Вакансии с зарплатой в диапазоне {salary_range} не найдены")
        else:
            print(f"\nНайдено {len(filtered)} вакансий с зарплатой в диапазоне {salary_range}:")
            print_vacancies(filtered)
    except Exception as e:
        print(f"Ошибка при фильтрации по зарплате: {e}")


def _handle_show_all(saver: JSONSaver) -> None:
    """Обработка показа всех сохраненных вакансий"""
    try:
        saved_data = saver.get_vacancies()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return

    if not saved_data:
        print("Нет сохраненных вакансий")
        return

    try:
        vacancies_list = Vacancy.cast_to_object_list(saved_data)
        print(f"\nВсе сохраненные вакансии ({len(vacancies_list)} шт.):")

        show_all = input("Показать все сразу? (y/n): ").lower()
        if show_all == 'y':
            print_vacancies(vacancies_list)
        else:
            # Показать с пагинацией
            page_size = 5
            for i in range(0, len(vacancies_list), page_size):
                page = vacancies_list[i: i + page_size]
                print_vacancies(page)

                if i + page_size < len(vacancies_list):
                    input("\nНажмите Enter для продолжения...")
    except Exception as e:
        print(f"Ошибка при отображении вакансий: {e}")


def _handle_delete_vacancy(saver: JSONSaver) -> None:
    """Обработка удаления вакансии"""
    vacancy_id = input("Введите ID вакансии для удаления: ").strip()

    if not vacancy_id:
        print("ID вакансии не может быть пустым")
        return

    try:
        saver.delete_vacancy(vacancy_id)
        print(f"Вакансия с ID {vacancy_id} удалена")
    except Exception as e:
        print(f"Ошибка при удалении вакансии: {e}")


def _handle_clear_all(saver: JSONSaver) -> None:
    """Обработка очистки всех вакансий"""
    confirm = input(
        "Вы уверены, что хотите удалить все вакансии? (y/n): "
    ).lower()

    if confirm == 'y':
        try:
            saver.clear_file()
            print("Все вакансии удалены")
        except Exception as e:
            print(f"Ошибка при очистке файла: {e}")
    else:
        print("Отменено")


if __name__ == "__main__":
    try:
        user_interaction()
    except KeyboardInterrupt:
        print("\n\nПрограмма завершена.")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        print("Программа завершена.")
