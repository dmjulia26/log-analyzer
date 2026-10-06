def parse_line(line):
    parts = line.split() #Превращает строку лога в словарь с именованными полями
    return {
        "date": parts[0],
        "time": parts[1],
        "method": parts[2],
        "path": parts[3],
        "status": int(parts[4]),
        "time_ms": int(parts[5].replace("ms", "")),
        "request_id": parts[6],
    }


def load_entries(path):
    """Читает лог-файл и возвращает список записей (словарей)."""
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            entries.append(parse_line(line))
    return entries


def count_by_field(entries, field):
    """Считает, сколько раз встречается каждое значение поля."""
    counts = {}
    for entry in entries:
        value = entry[field]
        counts[value] = counts.get(value, 0) + 1
    return counts


def get_time_ms(entry):
    """Ключ сортировки: время ответа запроса (мс)."""
    return entry["time_ms"]


def get_count(item):
    """Ключ сортировки: количество из пары (значение, количество)."""
    return item[1]


def slowest_requests(entries, limit=5):
    """Возвращает limit самых медленных запросов."""
    return sorted(entries, key=get_time_ms)[:limit]


def filter_by_status(entries, status):
    """Оставляет только записи с заданным кодом ответа."""
    result = []
    for entry in entries:
        if entry["status"] == status:
            result.append(entry)
    return result


def count_by_minute(entries):
    """Считает записи по минутам. Ключ: время в формате "ЧЧ:ММ"."""
    counts = {}
    for entry in entries:
        minute = entry["time"][:5]
        counts[minute] = counts.get(minute, 0) + 1
    return counts


def find_by_request_id(entries, request_id):
    """Ищет запись по request_id. Если не нашла, возвращает None."""
    for entry in entries:
        if entry["request_id"] == request_id:
            return entry
    return None