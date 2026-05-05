from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """全局配置（从环境变量 / .env 文件读取）。"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "AI Data Governance Platform"
    app_env: str = "dev"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    app_debug: bool = True

    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    default_tenant_id: str = "default"

    # 持久化：USE_MOCK=true 或 未配置 DATABASE_URL 时走内存 Mock（pytest / 本机 ./start.sh 默认）
    # Docker Compose 中应设置 USE_MOCK=false 且注入 DATABASE_URL
    use_mock: bool = True
    database_url: str | None = None
    redis_url: str | None = None

    @property
    def database_enabled(self) -> bool:
        if self.use_mock:
            return False
        return bool(self.database_url and self.database_url.strip())

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
