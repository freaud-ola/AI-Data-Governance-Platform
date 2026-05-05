from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应包装。"""

    success: bool = True
    code: int = 0
    message: str = "ok"
    data: T | None = None


class PageMeta(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=200)
    total: int = 0


class PageData(BaseModel, Generic[T]):
    items: list[T]
    meta: PageMeta
