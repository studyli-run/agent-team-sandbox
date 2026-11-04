from sandbox.app import response_for


def test_health():
    status, payload = response_for("/health")
    assert status == 200
    assert payload["status"] == "ok"
    assert "version" in payload


def test_unknown_path():
    status, payload = response_for("/missing")
    assert status == 404
    assert payload["status"] == "not_found"
