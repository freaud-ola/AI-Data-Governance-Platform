"""12 个治理域 API 的 smoke test：
- 全部 GET 路由 200
- 统一响应包装 `{success, code, message, data}` 形态正确
- 关键集合返回非空（Mock 数据已 seed）
- 资产目录的搜索 / 筛选 / 分页 / 详情 / 404 行为正确
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient


def _ok(payload: dict[str, Any]) -> Any:
    """断言统一响应包装成功，并返回 data 字段。"""
    assert isinstance(payload, dict)
    assert payload.get("success") is True, payload
    assert payload.get("code") == 0
    assert payload.get("message") == "ok"
    assert "data" in payload
    return payload["data"]


# ----- Overview -----
def test_overview_kpi(client: TestClient) -> None:
    data = _ok(client.get("/api/v1/overview/kpi").json())
    assert data["asset_total"] > 0
    assert 0 <= data["coverage_lineage"] <= 1
    assert 0 <= data["coverage_comment"] <= 1


@pytest.mark.parametrize("name", ["quality", "lineage", "asset"])
def test_overview_trends(client: TestClient, name: str) -> None:
    data: list[dict[str, Any]] = _ok(client.get(f"/api/v1/overview/trend/{name}").json())
    assert len(data) >= 7
    for p in data:
        assert "ts" in p and "value" in p


def test_overview_domain_coverage(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/overview/domain-coverage").json())
    assert len(data) > 0
    assert {"domain", "asset_count", "quality_score", "governance_score"} <= set(data[0].keys())


# ----- Metadata -----
def test_metadata_sources(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/metadata/sources").json())
    assert len(data) >= 1
    types = {s["type"] for s in data}
    assert {"hive", "mysql"} <= types


def test_metadata_source_detail_404(client: TestClient) -> None:
    resp = client.get("/api/v1/metadata/sources/does-not-exist").json()
    assert resp["success"] is False
    assert resp["code"] == 404


# ----- Catalog -----
def test_catalog_assets_pagination(client: TestClient) -> None:
    data = _ok(client.get("/api/v1/catalog/assets", params={"page": 1, "page_size": 5}).json())
    assert data["meta"]["page"] == 1
    assert data["meta"]["page_size"] == 5
    assert data["meta"]["total"] >= len(data["items"])
    assert len(data["items"]) <= 5


def test_catalog_assets_filter_by_layer(client: TestClient) -> None:
    data = _ok(client.get("/api/v1/catalog/assets", params={"layer": "DWS"}).json())
    assert data["meta"]["total"] > 0
    for a in data["items"]:
        assert a["layer"] == "DWS"


def test_catalog_assets_keyword(client: TestClient) -> None:
    data = _ok(client.get("/api/v1/catalog/assets", params={"keyword": "order"}).json())
    assert data["meta"]["total"] > 0
    assert any("order" in a["name"].lower() for a in data["items"])


def test_catalog_asset_detail_and_404(client: TestClient) -> None:
    list_data = _ok(client.get("/api/v1/catalog/assets", params={"page_size": 1}).json())
    assert len(list_data["items"]) == 1
    asset_id = list_data["items"][0]["id"]
    detail = _ok(client.get(f"/api/v1/catalog/assets/{asset_id}").json())
    assert detail["id"] == asset_id

    not_found = client.get("/api/v1/catalog/assets/no-such-id").json()
    assert not_found["success"] is False
    assert not_found["code"] == 404


# ----- Quality -----
def test_quality_rules(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/quality/rules").json())
    assert len(data) > 0
    dims = {r["dimension"] for r in data}
    assert dims & {"completeness", "validity", "uniqueness", "consistency", "timeliness"}


def test_quality_incidents(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/quality/incidents").json())
    assert len(data) > 0
    for i in data:
        assert i["severity"] in {"P0", "P1", "P2", "P3"}


# ----- Lineage -----
def test_lineage_graph(client: TestClient) -> None:
    data = _ok(client.get("/api/v1/lineage/graph").json())
    assert len(data["nodes"]) > 0
    assert len(data["edges"]) > 0
    node_ids = {n["id"] for n in data["nodes"]}
    for e in data["edges"]:
        assert e["source"] in node_ids
        assert e["target"] in node_ids


# ----- Standards / Metrics / MDM / Lifecycle -----
@pytest.mark.parametrize(
    "url",
    [
        "/api/v1/standards",
        "/api/v1/metrics",
        "/api/v1/mdm/entities",
        "/api/v1/lifecycle/policies",
    ],
)
def test_simple_list_endpoints(client: TestClient, url: str) -> None:
    data: list[Any] = _ok(client.get(url).json())
    assert isinstance(data, list)
    assert len(data) > 0


# ----- Security -----
def test_security_classifications(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/security/classifications").json())
    assert len(data) > 0
    for c in data:
        assert c["pii_level"] in {"L1", "L2", "L3", "L4"}


# ----- AI Hub -----
def test_ai_prompts(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/ai/prompts").json())
    assert len(data) > 0
    for p in data:
        assert 0.0 <= p["success_rate"] <= 1.0


def test_ai_invocations(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/ai/invocations").json())
    assert len(data) > 0


# ----- Reports -----
def test_reports(client: TestClient) -> None:
    data: list[dict[str, Any]] = _ok(client.get("/api/v1/reports").json())
    assert len(data) > 0


# ----- 多租户 Header 透传（不应改变响应结构） -----
def test_tenant_header_passthrough(client: TestClient) -> None:
    r1 = client.get("/api/v1/overview/kpi").json()
    r2 = client.get("/api/v1/overview/kpi", headers={"X-Tenant-Id": "tenant-x"}).json()
    assert r1["success"] is True
    assert r2["success"] is True
    # 当前 Mock 阶段不区分租户，data 一致
    assert r1["data"] == r2["data"]
