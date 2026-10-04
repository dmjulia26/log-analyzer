from pathlib import Path

log_file = Path(__file__).resolve().parent.parent / "data" / "sample_access.log"


def parse_line(line):
    parts = line.split()
    return {
        "date": parts[0],
        "time": parts[1],
        "method": parts[2],
        "path": parts[3],
        "status": int(parts[4]),
        "time_ms": int(parts[5].replace("ms", "")),
        "request_id": parts[6],
    }

#сортировка по времени
def get_time_ms(entry):
    return entry["time_ms"]

def get_count(item):
    return item[1]

# Читаем весь лог в список записей
entries = []
with open(log_file, encoding="utf-8") as f:
    for line in f:
        entries.append(parse_line(line))

# 1. Количество ответов по кодам
status_counts = {}
for entry in entries:
    status = entry["status"]
    status_counts[status] = status_counts.get(status, 0) + 1

print("Количество ответов по кодам:")
for status, count in sorted(status_counts.items()):
    print(f"  {status}: {count}")
print(f"Всего запросов: {len(entries)}")

# 2. Пять самых медленных запросов
slowest = sorted(entries, key=get_time_ms, reverse=True)[:5]

print("\nТоп-5 самых медленных запросов:")
for entry in slowest:
    print(f"  {entry['time_ms']} мс  {entry['method']} {entry['path']} {entry['status']} {entry['request_id']}")

# 3. Ошибки 500
errors_500 = []
for entry in entries:
    if entry["status"] == 500:
        errors_500.append(entry)

print(f"\nОшибок 500: {len(errors_500)}")
for entry in errors_500:
    print(f"  {entry['time']}  {entry['path']}  {entry['request_id']}")

# 4. Количество вызванных API
path_counts = {}
for entry in entries:
    path = entry['path']
    path_counts[path] = path_counts.get(path, 0) + 1
print("\nКоличество запросов по путям:")
for path, count in sorted(path_counts.items()):
    print(f"  {path}: {count}")

#5. Всплеск ошибок
errors_by_minute = {}
for entry in errors_500:
    minute = entry["time"][:5]
    errors_by_minute[minute] = errors_by_minute.get(minute, 0) + 1

print("\nОшибки 500 по минутам (по убыванию):")
for minute, count in sorted(errors_by_minute.items(), key=get_count, reverse=True):
    print(f"  {minute}: {count}")

# 6. Поиск запроса по request_id
search_id = input("\nВведите request_id (например, req-0042): ").strip()

found = None
for entry in entries:
    if entry["request_id"] == search_id:
        found = entry

if found is None:
    print("Запрос не найден")
else:
    for key, value in found.items():
        print(f"  {key}: {value}")