import random

methods = ["GET", "POST"]
paths = ["/api/v1/orders", "/api/v3/products", "/api/v1/sellers", "/api/v3/payments"]
statuses = [200, 200, 200, 201, 200, 404, 429, 503]

for i in range(1, 20):
    method = random.choice(methods)
    path = random.choice(paths)
    status = random.choice(statuses)
    time_ms = random.randint(20, 500)
    request_id = f"req-{i:04d}"

    line = f"2026-10-04 12:00:01 {method} {path} {status} {time_ms}ms {request_id}"
    print(line)