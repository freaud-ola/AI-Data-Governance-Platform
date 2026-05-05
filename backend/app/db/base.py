from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative SQLAlchemy 基类（供 ORM model 继承）。"""
