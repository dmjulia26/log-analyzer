from loganalyzer.log_analyzer import (
    count_by_field,
    filter_by_status,
    find_by_request_id,
    parse_line,
    slowest_requests,
)

# Небольшой набор записей для проверок
ENTRIES = [
    {"time": "12:00:01", "path": "/api/v1/orders", "status": 200, "time_ms": 50, "request_id": "req-0001"},
    {"time": "12:00:02", "path": "/api/v1/orders", "status": 500, "time_ms": 300, "request_id": "req-0002"},
    {"time": "12:00:03", "path": "/api/v1/sellers", "status": 200, "time_ms": 120, "request_id": "req-0003"},
]


def test_parse_line():
    line = "2026-10-04 12:00:03 GET /api/v1/orders 200 45ms req-0001"
    entry = parse_line(line)
    assert entry["method"] == "GET"
    assert entry["status"] == 200
    assert entry["time_ms"] == 45
    assert entry["request_id"] == "req-0001"


def test_count_by_field():
    result = count_by_field(ENTRIES, "status")
    assert result == {200: 2, 500: 1}


def test_filter_by_status():
    result = filter_by_status(ENTRIES, 500)
    assert len(result) == 1
    assert result[0]["request_id"] == "req-0002"


def test_slowest_requests():
    result = slowest_requests(ENTRIES, limit=2)
    assert result[0]["request_id"] == "req-0002"  # самый медленный: 300 мс
    assert result[1]["request_id"] == "req-0003"  # второй: 120 мс


def test_find_by_request_id():
    assert find_by_request_id(ENTRIES, "req-0003")["path"] == "/api/v1/sellers"
    assert find_by_request_id(ENTRIES, "req-9999") is None