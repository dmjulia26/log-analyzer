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


status_counts = {}
with open(log_file, encoding="utf-8") as f:
    for line in f:
        entry = parse_line(line)
        status = entry["status"]
        status_counts[status] = status_counts.get(status, 0) + 1

total = sum(status_counts.values())

print("Количество ответов по кодам:")
for status, count in sorted(status_counts.items()):
    print(f"  {status}: {count}")
print(f"Всего запросов: {total}")