"""多租户上下文工具。

按架构原则：所有 API 默认带 `tenant_id`，开发期默认 `default`。
正式版会从 SSO Token / 请求头解析。
"""


from fastapi import Header

from app.core.config import get_settings


async def get_tenant_id(x_tenant_id: str | None = Header(default=None)) -> str:
    if x_tenant_id:
        return x_tenant_id
    return get_settings().default_tenant_id
