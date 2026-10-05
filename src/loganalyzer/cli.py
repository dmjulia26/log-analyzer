"""Точка входа: запускает анализ лога и печатает результаты."""

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

LOG_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "sample_access.log"


def main():
    """Запускает анализ и печатает результаты."""
    entries = load_entries(LOG_FILE)

    print("Количество ответов по кодам:")
    for status, count in sorted(count_by_field(entries, "status").items()):
        print(f"  {status}: {count}")
    print(f"Всего запросов: {len(entries)}")

    print("\nТоп-5 самых медленных запросов:")
    for entry in slowest_requests(entries):
        print(f"  {entry['time_ms']} мс  {entry['method']} {entry['path']}  {entry['request_id']}")

    errors_500 = filter_by_status(entries, 500)
    print(f"\nОшибок 500: {len(errors_500)}")
    for entry in errors_500:
        print(f"  {entry['time']}  {entry['path']}  {entry['request_id']}")

    print("\nКоличество запросов по путям:")
    for path, count in sorted(count_by_field(entries, "path").items()):
        print(f"  {path}: {count}")

    print("\nОшибки 500 по минутам (по убыванию):")
    errors_by_minute = count_by_minute(errors_500)
    for minute, count in sorted(errors_by_minute.items(), key=get_count, reverse=True):
        print(f"  {minute}: {count}")

    search_id = input("\nВведите request_id (например, req-0042): ").strip()
    found = find_by_request_id(entries, search_id)
    if found is None:
        print("Запрос не найден")
    else:
        print("Найден запрос:")
        for key, value in found.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()