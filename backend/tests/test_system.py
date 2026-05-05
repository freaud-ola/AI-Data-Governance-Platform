"""系统级冒烟测试：根路径、健康检查、OpenAPI。"""

from __future__ import annotations

from fastapi.testclient import TestClient


def test_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["service"]
    assert body["version"]
    assert body.get("persistence") in ("mock", "postgres")


def test_root(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    body = resp.json()
    assert body["service"]
    assert body["docs"] == "/docs"


def test_openapi(client: TestClient) -> None:
    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    spec = resp.json()
    assert spec["openapi"].startswith("3.")
    paths = spec["paths"]
    # 12 个治理域路由前缀必须存在
    expected_prefixes = {
        "/api/v1/overview/",
        "/api/v1/metadata/",
        "/api/v1/catalog/",
        "/api/v1/quality/",
        "/api/v1/lineage/",
        "/api/v1/standards",
        "/api/v1/metrics",
        "/api/v1/mdm/",
        "/api/v1/lifecycle/",
        "/api/v1/security/",
        "/api/v1/ai/",
        "/api/v1/reports",
    }
    found = {p for p in paths.keys()}
    for prefix in expected_prefixes:
        assert any(p.startswith(prefix) for p in found), f"missing route prefix: {prefix}"
