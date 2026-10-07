"""Работа с базой SQLite: сохранение записей лога и SQL-запросы."""

import sqlite3


def create_connection(db_path):
    """Открывает базу (создаёт файл, если его нет) и готовит таблицу requests."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS requests (
            request_id TEXT PRIMARY KEY,
            date TEXT,
            time TEXT,
            method TEXT,
            path TEXT,
            status INTEGER,
            time_ms INTEGER
        )
        """
    )
    return conn


def save_entries(conn, entries):
    """Заменяет содержимое таблицы записями из списка entries."""
    conn.execute("DELETE FROM requests")  # чистим старое, чтобы повторный запуск не дублировал данные
    rows = [
        (e["request_id"], e["date"], e["time"], e["method"], e["path"], e["status"], e["time_ms"])
        for e in entries
    ]
    conn.executemany("INSERT INTO requests VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    conn.commit()


def errors_by_path(conn):
    """Возвращает пары (путь, число ошибок 5xx), сначала самые проблемные."""
    cursor = conn.execute(
        """
        SELECT path, COUNT(*) AS errors
        FROM requests
        WHERE status >= 500
        GROUP BY path
        ORDER BY errors DESC
        """
    )
    return cursor.fetchall()


def avg_time_by_path(conn):
    """Возвращает тройки (путь, среднее время, максимальное время), сначала самые медленные."""
    cursor = conn.execute(
        """
        SELECT path, ROUND(AVG(time_ms), 1), MAX(time_ms)
        FROM requests
        GROUP BY path
        ORDER BY AVG(time_ms) DESC
        """
    )
    return cursor.fetchall()