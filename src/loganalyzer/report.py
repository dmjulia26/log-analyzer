"""Генерация markdown-отчёта по результатам анализа."""

from datetime import datetime
from loganalyzer.log_analyzer import get_count

def build_report(entries, status_counts, slowest, errors_by_path_rows, errors_by_minute):
    """Собирает markdown-текст отчёта и возвращает его одной строкой."""
    lines = []
    lines.append("# Отчёт по access-логу")
    lines.append("")
    lines.append(f"Сформирован: {datetime.now():%Y-%m-%d %H:%M}")
    lines.append(f"Всего запросов: {len(entries)}")
    lines.append("")

    lines.append("## Коды ответов")
    lines.append("")
    lines.append("| Код | Количество |")
    lines.append("|---|---|")
    for status, count in sorted(status_counts.items()):
        lines.append(f"| {status} | {count} |")
    lines.append("")

    lines.append("## Самые медленные запросы")
    lines.append("")
    lines.append("| Время, мс | Запрос | request_id |")
    lines.append("|---|---|---|")
    for entry in slowest:
        lines.append(
            f"| {entry['time_ms']} | {entry['method']} {entry['path']} | {entry['request_id']} |"
        )
    lines.append("")

    lines.append("## Ошибки 5xx по путям")
    lines.append("")
    lines.append("| Путь | Ошибок |")
    lines.append("|---|---|")
    for path, errors in errors_by_path_rows:
        lines.append(f"| {path} | {errors} |")
    lines.append("")
    lines.append("## Ошибки 500 по минутам (топ-5)")
    lines.append("")
    lines.append("| Минута | Ошибок |")
    lines.append("|---|---|")

    for minute, count in sorted(errors_by_minute.items(), key=get_count, reverse=True)[:5]:
        lines.append(f"| {minute} | {count} |")
    return "\n".join(lines)