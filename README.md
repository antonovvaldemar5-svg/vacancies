if (!(Test-Path README.md)) {
    @"
# Парсер вакансий с HH.ru

Курсовой проект для работы с API.

## Функционал
- Поиск вакансий на HH.ru
- Сохранение в JSON файл
- Фильтрация по зарплате
- Поиск по ключевым словам
- Консольный интерфейс

## Запуск
\`\`\`bash
# Установите зависимости
pip install -r requirements.txt

# Запустите программу
python -m src.main
\`\`\`

## Тестирование
\`\`\`bash
pytest tests/ -v
\`\`\`
"@ | Out-File -FilePath README.md -Encoding UTF8
    git add README.md
}
