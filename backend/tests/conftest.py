"""pytest 公共夹具：构造 FastAPI TestClient（基于 httpx，不需要真启动端口）。"""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
