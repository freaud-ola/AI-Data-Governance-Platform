from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def init_engine(url: str) -> None:
    global _engine, _SessionLocal
    dispose_engine()
    _engine = create_engine(url, pool_pre_ping=True, pool_size=5, max_overflow=10)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def dispose_engine() -> None:
    global _engine, _SessionLocal
    if _engine is not None:
        _engine.dispose()
    _engine = None
    _SessionLocal = None


def session_factory() -> sessionmaker[Session]:
    if _SessionLocal is None:
        raise RuntimeError("database engine not initialized — call init_engine() first")
    return _SessionLocal


def db_session_dependency() -> Generator[Session | None, None, None]:
    """FastAPI Depends：成功请求末 commit；异常 rollback。"""
    if _SessionLocal is None:
        yield None
        return
    session = _SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
