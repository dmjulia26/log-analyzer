# Log Analyzer

Консольный инструмент на Python для разбора access-логов: помогает быстро понять, что происходило в системе во время инцидента. 
Учебный проект, собранный по мотивам рабочих задач сопровождения: анализ логов, поиск запроса по `request_id`, выгрузка в SQL и отчёт.

## Что умеет

- считает ответы по кодам (200, 404, 500 и т.д.);
- показывает самые медленные запросы;
- находит ошибки 500 и показывает, в какие минуты их было больше всего;
- ищет запрос по `request_id`;
- фильтрует запросы по коду ответа;
- сохраняет записи в SQLite и строит отчёт SQL-запросами (ошибки 5xx по путям, среднее и максимальное время ответа);
- формирует markdown-отчёт.

## Формат лога

```
2026-10-04 12:00:03 GET /api/v1/orders 200 45ms req-0001
```

Дата, время, метод, путь, код ответа, время ответа, `request_id`. Тестовый лог создаётся скриптом `scripts/generate_logs.py`.

## Технологии

Python 3, `argparse`, `sqlite3`, `pytest`, Git.

## Установка

```
git clone <ссылка на репозиторий>
cd <папка проекта>
python -m venv .venv
.venv\Scripts\activate
pip install pytest
python scripts/generate_logs.py
```

## Использование

Команды запускаются из папки `src`:

```
cd src
python -m loganalyzer.cli                       # полный отчёт в консоль
python -m loganalyzer.cli --top 3               # топ-3 самых медленных запросов
python -m loganalyzer.cli --find req-0042       # найти запрос по request_id
python -m loganalyzer.cli --status 404          # все запросы с кодом 404
python -m loganalyzer.cli --sql                 # SQL-отчёт (SQLite)
python -m loganalyzer.cli --report              # markdown-отчёт в data/report.md
python -m loganalyzer.cli --help                # справка
```

Пример готового отчёта: [data/report.md](data/report.md).

## Тесты

Из корня проекта:

```
python -m pytest
```

## Структура проекта

```
data/            тестовый лог и отчёт
scripts/         генератор тестовых логов
src/loganalyzer/
    cli.py           командная строка
    log_analyzer.py  разбор и анализ логов
    storage.py       SQLite и SQL-запросы
    report.py        markdown-отчёт
tests/           тесты на pytest
```

## Что дальше

- проверка доступности API (коды ответа, время, ретраи);
- тесты для отчёта и SQL-части;
- уведомления при всплеске ошибок.