"""程序内调用 Alembic upgrade（容器启动时可自动补齐 schema）。"""

from __future__ import annotations

from pathlib import Path

from alembic.config import Config

from alembic import command


def alembic_upgrade_head() -> None:
    backend_root = Path(__file__).resolve().parent.parent.parent
    ini_path = backend_root / "alembic.ini"
    alembic_dir = backend_root / "alembic"
    cfg = Config(str(ini_path))
    cfg.set_main_option("script_location", str(alembic_dir))
    command.upgrade(cfg, "head")
