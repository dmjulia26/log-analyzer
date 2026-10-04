import random
from datetime import datetime, timedelta
from pathlib import Path

methods = ["GET", "POST"]
paths = ["/api/v1/orders", "/api/v3/products", "/api/v1/sellers", "/api/v3/payments"]
statuses = [200, 200, 200, 201, 200, 404, 429, 500, 503]

output_file = Path(__file__).resolve().parent.parent / "data" / "sample_access.log"
output_file.parent.mkdir(exist_ok=True)

current_time = datetime(2026, 10, 4, 12, 0, 0)

with open(output_file, "w", encoding="utf-8") as f:
    for i in range(1, 501):
        current_time += timedelta(seconds=random.randint(1, 5))
        method = random.choice(methods)
        path = random.choice(paths)
        status = random.choice(statuses)
        time_ms = random.randint(20, 1000)
        request_id = f"req-{i:04d}"

        line = f"{current_time:%Y-%m-%d %H:%M:%S} {method} {path} {status} {time_ms}ms {request_id}"
        f.write(line + "\n")

print(f"Готово: записано 200 строк в {output_file}")