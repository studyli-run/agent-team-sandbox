import json
from http.client import HTTPConnection
from threading import Thread

from sandbox.app import Handler, ThreadingHTTPServer, response_for


def test_health():
    status, payload = response_for("/health")
    assert status == 200
    assert payload["status"] == "ok"
    assert "version" in payload


def test_unknown_path():
    status, payload = response_for("/missing")
    assert status == 404
    assert payload["status"] == "not_found"


def _run_get(path, monkeypatch):
    records = []

    def capture(event, **fields):
        records.append({"event": event, **fields})

    monkeypatch.setattr("sandbox.app.log", capture)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        port = server.server_address[1]
        conn = HTTPConnection("127.0.0.1", port, timeout=2)
        conn.request("GET", path)
        response = conn.getresponse()
        body = json.loads(response.read().decode())
        conn.close()
        return response.status, body, records
    finally:
        server.shutdown()
        thread.join(timeout=2)


def test_request_log_path_strips_query(monkeypatch):
    status, body, records = _run_get("/health?x=1", monkeypatch)
    assert status == 200
    assert body["status"] == "ok"
    request_logs = [r for r in records if r["event"] == "request"]
    assert len(request_logs) == 1
    assert request_logs[0]["path"] == "/health"
    assert "?" not in request_logs[0]["path"]


def test_request_log_path_without_query(monkeypatch):
    status, body, records = _run_get("/health", monkeypatch)
    assert status == 200
    assert body["status"] == "ok"
    request_logs = [r for r in records if r["event"] == "request"]
    assert len(request_logs) == 1
    assert request_logs[0]["path"] == "/health"


def test_health_query_matches_plain_route(monkeypatch):
    with_query = _run_get("/health?x=1", monkeypatch)
    plain = _run_get("/health", monkeypatch)
    assert with_query[0] == plain[0] == 200
    assert with_query[1] == plain[1]
