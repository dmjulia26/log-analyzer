"""Точка входа: разбирает аргументы командной строки и печатает результаты."""

import argparse
from pathlib import Path

from loganalyzer.log_analyzer import (
    count_by_field,
    count_by_minute,
    filter_by_status,
    find_by_request_id,
    get_count,
    load_entries,
    slowest_requests,
)
from loganalyzer.report import build_report
from loganalyzer.storage import (
    avg_time_by_path,
    create_connection,
    errors_by_path,
    save_entries,
)

# Лог, база и отчёт лежат в папке data в корне проекта
DEFAULT_LOG = Path(__file__).resolve().parent.parent.parent / "data" / "sample_access.log"
DEFAULT_DB = Path(__file__).resolve().parent.parent.parent / "data" / "logs.db"
DEFAULT_REPORT = Path(__file__).resolve().parent.parent.parent / "data" / "report.md"


def parse_args():
    """Описывает аргументы командной строки и возвращает введённые значения."""
    parser = argparse.ArgumentParser(description="Анализатор access-логов")
    parser.add_argument(
        "log_file",
        nargs="?",
        default=DEFAULT_LOG,
        help="путь к лог-файлу",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=5,
        help="сколько самых медленных запросов показать (по умолчанию 5)",
    )
    parser.add_argument(
        "--find",
        metavar="REQUEST_ID",
        help="найти один запрос по request_id и выйти",
    )
    parser.add_argument(
        "--status",
        type=int,
        help="список запросов с выбранным кодом ответа",
    )
    parser.add_argument(
        "--sql",
        action="store_true",
        help="сохранить записи в SQLite и показать SQL-отчёт",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="сохранить markdown-отчёт в data/report.md",
    )
    return parser.parse_args()


def print_request(entry):
    """Печатает все поля одной записи."""
    for key, value in entry.items():
        print(f"  {key}: {value}")


def main():
    """Запускает анализ и печатает результаты."""
    args = parse_args()
    entries = load_entries(args.log_file)

    # Режим поиска: нашли запрос, показали и закончили работу
    if args.find:
        found = find_by_request_id(entries, args.find)
        if found is None:
            print("Запрос не найден")
        else:
            print("Найден запрос:")
            print_request(found)
        return

    # Режим фильтра: показать только запросы с выбранным кодом ответа
    if args.status:
        filtered = filter_by_status(entries, args.status)
        print(f"Запросов с кодом {args.status}: {len(filtered)}")
        for entry in filtered:
            print(f"  {entry['time']}  {entry['method']} {entry['path']}  {entry['request_id']}")
        return

    # Режим SQL: сохраняем записи в базу и считаем отчёт запросами
    if args.sql:
        conn = create_connection(DEFAULT_DB)
        save_entries(conn, entries)
        print(f"Сохранено записей в базу: {len(entries)}")

        print("\nОшибки 5xx по путям (SQL):")
        for path, errors in errors_by_path(conn):
            print(f"  {path}: {errors}")

        print("\nВремя ответа по путям (SQL), среднее / максимум, мс:")
        for path, avg_ms, max_ms in avg_time_by_path(conn):
            print(f"  {path}: {avg_ms} / {max_ms}")

        conn.close()
        return

    # Режим отчёта в файл: собираем markdown и сохраняем
    if args.report:
        conn = create_connection(DEFAULT_DB)
        save_entries(conn, entries)
        report = build_report(
            entries,
            count_by_field(entries, "status"),
            slowest_requests(entries, args.top),
            errors_by_path(conn),
            count_by_minute(filter_by_status(entries, 500)),
        )
        conn.close()
        DEFAULT_REPORT.write_text(report, encoding="utf-8")
        print(f"Отчёт сохранён: {DEFAULT_REPORT}")
        return

    # Режим отчёта в консоль
    print("Количество ответов по кодам:")
    for status, count in sorted(count_by_field(entries, "status").items()):
        print(f"  {status}: {count}")
    print(f"Всего запросов: {len(entries)}")

    print(f"\nТоп-{args.top} самых медленных запросов:")
    for entry in slowest_requests(entries, args.top):
        print(f"  {entry['time_ms']} мс  {entry['method']} {entry['path']}  {entry['request_id']}")

    errors_500 = filter_by_status(entries, 500)
    print(f"\nОшибок 500: {len(errors_500)}")
    for entry in errors_500[:args.top]:
        print(f"  {entry['time']}  {entry['path']}  {entry['request_id']}")

    print("\nКоличество запросов по путям:")
    for path, count in sorted(count_by_field(entries, "path").items()):
        print(f"  {path}: {count}")

    print("\nОшибки 500 по минутам (по убыванию):")
    errors_by_minute = count_by_minute(errors_500)
    for minute, count in sorted(errors_by_minute.items(), key=get_count, reverse=True):
        print(f"  {minute}: {count}")


if __name__ == "__main__":
    main()